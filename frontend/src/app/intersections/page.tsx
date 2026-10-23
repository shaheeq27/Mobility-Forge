"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/layout/app-shell";

type Observation = {
  source_page: number;
  source_row: string;
  section_no: number;
  road_section: string;
  configuration: string;
  period: string;
  direction: string;
  volume_pcu: string;
  vc_ratio: string;
  los: string;
};

type Validation = {
  valid: boolean;
  observation_count: number;
  issues: { code: string; message: string; source_row?: string | null }[];
};

const API_URL = (process.env.NEXT_PUBLIC_MOBILITY_API_URL ?? "http://localhost:8000").replace(/\/$/, "");

function label(value: string) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export default function Page() {
  const [observations, setObservations] = useState<Observation[]>([]);
  const [validation, setValidation] = useState<Validation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [observationsResponse, validationResponse] = await Promise.all([
          fetch(`${API_URL}/observations`),
          fetch(`${API_URL}/observations/validation`),
        ]);
        if (!observationsResponse.ok || !validationResponse.ok) {
          throw new Error("The MobilityForge API could not provide the observation data.");
        }
        const [records, validationResult] = await Promise.all([
          observationsResponse.json() as Promise<Observation[]>,
          validationResponse.json() as Promise<Validation>,
        ]);
        setObservations(records);
        setValidation(validationResult);
      } catch (requestError) {
        setError(requestError instanceof Error ? requestError.message : "Unable to load observations.");
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, []);

  return (
    <AppShell title="Intersections" path="/intersections">
      <p className="eyebrow">Source observations</p>
      <h2 className="heading">Six road sections, preserved by period and direction.</h2>
      <p className="sub">A read-only view of the verified Table 8 extract. This page reports observations and validation status only; it does not calculate priorities.</p>

      {validation && (
        <section className="notice" aria-label="Source validation status">
          <div>
            <b>{validation.valid ? "Source validation passed" : "Source validation needs review"}</b>
            {validation.valid
              ? `${validation.observation_count} observations loaded from the source extract. Methodology and rankings remain separate decisions.`
              : `${validation.issues.length} validation issue${validation.issues.length === 1 ? "" : "s"} returned by the backend. No ranking is available.`}
          </div>
        </section>
      )}

      {loading && <section className="panel" aria-live="polite"><h3 className="title">Loading observations…</h3><p className="desc">Connecting to the read-only MobilityForge API.</p></section>}
      {error && <section className="panel" role="alert"><h3 className="title">Observations unavailable</h3><p className="desc">{error}</p><p className="caption">Start the backend API and check NEXT_PUBLIC_MOBILITY_API_URL if this persists.</p></section>}
      {!loading && !error && observations.length === 0 && <section className="panel"><h3 className="title">No observations returned</h3><p className="desc">The API responded successfully but supplied no records.</p></section>}
      {!loading && !error && observations.length > 0 && (
        <section className="panel" aria-label="Traffic observations">
          <div className="table-wrap">
            <table className="data-table">
              <thead><tr><th>Section</th><th>Period</th><th>Direction</th><th>PCU volume</th><th>V/C</th><th>LOS</th></tr></thead>
              <tbody>{observations.map((observation) => (
                <tr key={`${observation.section_no}-${observation.period}-${observation.direction}`}>
                  <td><b>{observation.road_section}</b><small className="table-meta">Section {observation.section_no} · {observation.configuration}</small></td>
                  <td>{label(observation.period)}</td>
                  <td>{label(observation.direction)}</td>
                  <td>{Number(observation.volume_pcu).toLocaleString()}</td>
                  <td>{Number(observation.vc_ratio).toFixed(2)}</td>
                  <td><span className="chip">{observation.los}</span></td>
                </tr>
              ))}</tbody>
            </table>
          </div>
          <p className="caption">Source: BBMP Table 8, PDF page {observations[0].source_page}. Exact Table 8 clock-time windows remain unresolved.</p>
        </section>
      )}
    </AppShell>
  );
}
