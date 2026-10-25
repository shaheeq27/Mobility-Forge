/** Interface copy only. It makes no intervention-effectiveness claim. */
export const overviewMetrics = [
  ["Source observations", "24", "Preserved by period and direction", "var(--cyan)"],
  ["Road-section alternatives", "6", "Tumkur Road scope remains provisional", "var(--lime)"],
  ["Separate decision runs", "4", "Morning/evening × both directions", "var(--cyan)"],
  ["Research status", "Provisional", "Evidence and methodology remain under review", "var(--lime)"],
] as const;

export const overviewRows = [
  ["Source record", "BBMP Table 8 extract", "Available in the Intersections workspace"],
  ["Decision model", "Fuzzy TOPSIS execution", "Requires explicit weights and acknowledgement"],
  ["Interpretation", "LOS is contextual", "Not silently added as a weighted criterion"],
] as const;
