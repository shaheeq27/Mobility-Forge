export const API_URL = (process.env.NEXT_PUBLIC_MOBILITY_API_URL ?? "http://localhost:8000").replace(/\/$/, "");

export type Period = "morning" | "evening";
export type Direction = "towards_yeshwanthpur" | "towards_nagasandra";
export type Weights = { pcu: string; vc: string };
export type Observation = {
  source_page: number; source_row: string; section_no: number; road_section: string;
  configuration: string; period: Period; direction: Direction; volume_pcu: string; vc_ratio: string; los: string;
};
export type DecisionAlternative = {
  section_no: number; road_section: string; configuration: string; source_page: number; source_row: string;
  volume_pcu: string; vc_ratio: string; los: string; closeness_coefficient: string; rank: number;
};
export type DecisionResult = {
  methodology_version: string; provisional: boolean; disclosure: string; period: Period; direction: Direction;
  criteria: string[]; weights: Record<string, string>; alternatives: DecisionAlternative[];
};

export async function runDecision(period: Period, direction: Direction, weights: Weights): Promise<DecisionResult> {
  const response = await fetch(`${API_URL}/decision-engine/run`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ period, direction, weights, acknowledge_provisional: true }),
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail ?? "The decision run could not be completed.");
  return payload as DecisionResult;
}

export async function loadObservations(): Promise<Observation[]> {
  const response = await fetch(`${API_URL}/observations`);
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail ?? "Observations could not be loaded.");
  return payload as Observation[];
}

export function validateWeights(weights: Weights): string | null {
  const pcu = Number(weights.pcu); const vc = Number(weights.vc);
  if (!Number.isFinite(pcu) || !Number.isFinite(vc) || pcu < 0 || vc < 0) return "Weights must be finite and non-negative.";
  if (Math.abs(pcu + vc - 1) > 1e-10) return "Weights must sum exactly to 1.";
  return null;
}

export const RUNS: Array<{ label: string; period: Period; direction: Direction }> = [
  { label: "Morning · towards Yeshwanthpur", period: "morning", direction: "towards_yeshwanthpur" },
  { label: "Morning · towards Nagasandra", period: "morning", direction: "towards_nagasandra" },
  { label: "Evening · towards Yeshwanthpur", period: "evening", direction: "towards_yeshwanthpur" },
  { label: "Evening · towards Nagasandra", period: "evening", direction: "towards_nagasandra" },
];

export const SCENARIOS: Array<{ id: string; label: string; pcu: string; vc: string }> = [
  { id: "S0", label: "Equal baseline", pcu: "0.50", vc: "0.50" },
  { id: "S1", label: "PCU emphasis", pcu: "0.70", vc: "0.30" },
  { id: "S2", label: "V/C emphasis", pcu: "0.30", vc: "0.70" },
  { id: "S3", label: "PCU-only robustness", pcu: "1.00", vc: "0.00" },
  { id: "S4", label: "V/C-only robustness", pcu: "0.00", vc: "1.00" },
];
