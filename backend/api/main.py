"""FastAPI surface for source observations and the provisional decision run."""

from __future__ import annotations

import os
from decimal import Decimal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from mobility_engine.loader import DEFAULT_DATASET, load_observations
from mobility_engine.models import SectionObservation
from mobility_engine.validation import ValidationIssue, validate_observations
from mobility_engine.decision_service import DecisionResult, run_fuzzy_topsis


def _cors_origins() -> list[str]:
    configured = os.getenv("MOBILITY_FRONTEND_ORIGINS")
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return ["http://localhost:3000", "http://127.0.0.1:3000"]


class HealthResponse(BaseModel):
    status: str
    service: str
    research_data: str


class ObservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_page: int
    source_row: str
    section_no: int
    road_section: str
    configuration: str
    period: str
    direction: str
    volume_pcu: Decimal
    vc_ratio: Decimal
    los: str

    @classmethod
    def from_observation(cls, observation: SectionObservation) -> "ObservationResponse":
        return cls(
            source_page=observation.source_page,
            source_row=observation.source_row,
            section_no=observation.section_no,
            road_section=observation.road_section,
            configuration=observation.configuration,
            period=observation.period.value,
            direction=observation.direction.value,
            volume_pcu=observation.volume_pcu,
            vc_ratio=observation.vc_ratio,
            los=observation.los,
        )


class ValidationIssueResponse(BaseModel):
    code: str
    message: str
    source_row: str | None = None

    @classmethod
    def from_issue(cls, issue: ValidationIssue) -> "ValidationIssueResponse":
        return cls(code=issue.code, message=issue.message, source_row=issue.source_row)


class ValidationResponse(BaseModel):
    valid: bool
    observation_count: int
    issues: list[ValidationIssueResponse]


class DecisionRequest(BaseModel):
    period: str
    direction: str
    weights: dict[str, Decimal]
    acknowledge_provisional: bool = False


class FuzzyNumberResponse(BaseModel):
    lower: Decimal
    modal: Decimal
    upper: Decimal


class DecisionAlternativeResponse(BaseModel):
    section_no: int
    road_section: str
    configuration: str
    source_page: int
    source_row: str
    volume_pcu: Decimal
    vc_ratio: Decimal
    los: str
    normalized: dict[str, FuzzyNumberResponse]
    weighted: dict[str, FuzzyNumberResponse]
    distance_positive: Decimal
    distance_negative: Decimal
    closeness_coefficient: Decimal
    rank: int


class DecisionResponse(BaseModel):
    methodology_version: str
    provisional: bool
    disclosure: str
    period: str
    direction: str
    criteria: list[str]
    weights: dict[str, Decimal]
    alternatives: list[DecisionAlternativeResponse]


app = FastAPI(
    title="MobilityForge Read-Only API",
    description="Source observation access, integrity status, and explicitly acknowledged provisional model execution.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Accept", "Content-Type"],
)


def _load_source() -> list[SectionObservation]:
    try:
        return load_observations(DEFAULT_DATASET)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail="source observation data is unavailable") from exc
    except (OSError, ValueError) as exc:
        raise HTTPException(status_code=503, detail="source observation data could not be loaded") from exc
    except Exception as exc:  # pragma: no cover - defensive boundary for client safety
        raise HTTPException(status_code=500, detail="unexpected source-data failure") from exc


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="mobilityforge-api",
        research_data="not evaluated by health check",
    )


@app.get("/observations", response_model=list[ObservationResponse])
def observations() -> list[ObservationResponse]:
    return [ObservationResponse.from_observation(item) for item in _load_source()]


@app.get("/observations/validation", response_model=ValidationResponse)
def observations_validation() -> ValidationResponse:
    loaded = _load_source()
    try:
        issues = validate_observations(loaded)
    except Exception as exc:  # pragma: no cover - defensive boundary for client safety
        raise HTTPException(status_code=500, detail="unexpected validation failure") from exc
    return ValidationResponse(
        valid=not issues,
        observation_count=len(loaded),
        issues=[ValidationIssueResponse.from_issue(issue) for issue in issues],
    )


def _fuzzy_response(value):
    return FuzzyNumberResponse(lower=value.lower, modal=value.modal, upper=value.upper)


def _decision_response(result: DecisionResult) -> DecisionResponse:
    return DecisionResponse(
        methodology_version="phase9-provisional-v1",
        provisional=True,
        disclosure=("Provisional execution only: instructor approval, exact Table 8 peak windows, "
                    "and research weight/TFN decisions remain unresolved. This is not an intervention finding."),
        period=result.period.value,
        direction=result.direction.value,
        criteria=["pcu", "vc"],
        weights=result.weights,
        alternatives=[
            DecisionAlternativeResponse(
                section_no=item.observation.section_no,
                road_section=item.observation.road_section,
                configuration=item.observation.configuration,
                source_page=item.observation.source_page,
                source_row=item.observation.source_row,
                volume_pcu=item.observation.volume_pcu,
                vc_ratio=item.observation.vc_ratio,
                los=item.observation.los,
                normalized={name: _fuzzy_response(value) for name, value in item.normalized.items()},
                weighted={name: _fuzzy_response(value) for name, value in item.weighted.items()},
                distance_positive=item.distance_positive,
                distance_negative=item.distance_negative,
                closeness_coefficient=item.closeness_coefficient,
                rank=item.rank,
            )
            for item in result.alternatives
        ],
    )


@app.post("/decision-engine/run", response_model=DecisionResponse)
def decision_engine_run(request: DecisionRequest) -> DecisionResponse:
    if not request.acknowledge_provisional:
        raise HTTPException(status_code=400, detail="explicit provisional acknowledgement is required")
    try:
        from mobility_engine.models import Direction, Period
        period = Period(request.period)
        direction = Direction(request.direction)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="period or direction is invalid") from exc
    loaded = _load_source()
    try:
        issues = validate_observations(loaded)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail="unexpected validation failure") from exc
    if issues:
        raise HTTPException(status_code=503, detail="source observations failed integrity validation")
    selected = [item for item in loaded if item.period == period and item.direction == direction]
    try:
        result = run_fuzzy_topsis(selected, period, direction, request.weights)
    except (ValueError, ArithmeticError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return _decision_response(result)
