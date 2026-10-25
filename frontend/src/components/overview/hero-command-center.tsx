"use client";

import Link from "next/link";
import { useState } from "react";

const runs = [
  { id: "morning-yeshwanthpur", period: "Morning", direction: "Towards Yeshwanthpur", short: "AM · Yeshwanthpur" },
  { id: "morning-nagasandra", period: "Morning", direction: "Towards Nagasandra", short: "AM · Nagasandra" },
  { id: "evening-yeshwanthpur", period: "Evening", direction: "Towards Yeshwanthpur", short: "PM · Yeshwanthpur" },
  { id: "evening-nagasandra", period: "Evening", direction: "Towards Nagasandra", short: "PM · Nagasandra" },
] as const;

type Run = (typeof runs)[number];

export function HeroCommandCenter() {
  const [selected, setSelected] = useState<Run>(runs[0]);

  return (
    <section className="command-hero" aria-labelledby="overview-title">
      <div className="command-hero-grid" aria-hidden="true" />
      <div className="command-hero-glow command-hero-glow-one" aria-hidden="true" />
      <div className="command-hero-glow command-hero-glow-two" aria-hidden="true" />

      <div className="command-copy">
        <div className="command-kicker"><span className="live-dot" /> Urban Mobility Intelligence</div>
        <h2 id="overview-title">Build better mobility decisions, one transparent run at a time.</h2>
        <p>Explore verified observations, configure a documented model, and inspect provisional outputs without blurring evidence into conclusions.</p>
        <div className="command-actions">
          <Link className="hero-primary" href="/decision-engine">Configure a decision run <span>→</span></Link>
          <Link className="hero-secondary" href="/intersections">Inspect source records</Link>
        </div>
        <div className="command-proof"><span>24 source observations</span><i /> <span>6 road sections</span><i /> <span>4 separate runs</span></div>
      </div>

      <aside className="run-console" aria-label="Select a provisional source slice">
        <div className="console-header"><div><span>Decision workspace</span><b>Choose a source slice</b></div><em>Provisional</em></div>
        <div className="route-visual" aria-hidden="true">
          <svg viewBox="0 0 320 116" fill="none"><path d="M13 87C59 81 61 31 108 35s42 52 90 44c38-6 41-42 108-46" /><path className="route-visual-faint" d="M20 101C66 95 77 55 120 58s47 38 86 29c42-10 43-47 100-57" /><circle cx="13" cy="87" r="5" /><circle cx="108" cy="35" r="5" /><circle cx="198" cy="79" r="5" /><circle cx="306" cy="33" r="5" /></svg>
          <span className="route-pulse" />
        </div>
        <div className="run-selector" role="group" aria-label="Period and direction">
          {runs.map((run) => <button key={run.id} type="button" className={selected.id === run.id ? "run-option is-selected" : "run-option"} onClick={() => setSelected(run)} aria-pressed={selected.id === run.id}><span>{run.period}</span><b>{run.direction.replace("Towards ", "")}</b></button>)}
        </div>
        <div className="selected-run"><span>Selected analytical slice</span><b>{selected.short}</b><p>Its period and direction stay separate from the other three source runs.</p></div>
      </aside>
    </section>
  );
}
