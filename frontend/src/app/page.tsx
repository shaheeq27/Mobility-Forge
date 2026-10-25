import { AppShell } from "@/components/layout/app-shell";
import { Icon } from "@/components/ui/icons";
import { HeroCommandCenter } from "@/components/overview/hero-command-center";
import { overviewMetrics, overviewRows } from "@/lib/demo-data";

const workflow = [
  ["01", "Inspect the evidence", "Review the preserved PCU, V/C, period, direction, and LOS observations before a decision run."],
  ["02", "Set an explicit scenario", "Choose one source-labelled period/direction slice and supply transparent criterion weights."],
  ["03", "Read outputs in context", "Compare provisional rankings and sensitivity behaviour without claiming intervention effectiveness."],
];

export default function Home() {
  return (
    <AppShell title="Overview" path="/">
      <HeroCommandCenter />

      <section className="notice" aria-label="Research interpretation notice">
        <Icon name="notice" size={17} />
        <div><b>Interpret outputs with care</b>The dashboard exposes source-backed observations and provisional calculations. Method approval, weight policy, and exact Table 8 peak windows remain open research decisions.</div>
      </section>

      <section className="metrics" aria-label="Project status overview">
        {overviewMetrics.map(([label, value, caption, accent]) => (
          <article className="metric" style={{ "--accent": accent } as React.CSSProperties} key={label}>
            <div className="label">{label}</div><div className="value">{value}</div><div className="caption">{caption}</div>
          </article>
        ))}
      </section>

      <section className="columns">
        <article className="panel">
          <h3 className="title">Research workflow</h3>
          <p className="desc">A disciplined route from source records to an explainable screening model.</p>
          {workflow.map(([number, title, description]) => (
            <div className="step" key={number}><div className="num">{number}</div><div><b>{title}</b><p>{description}</p></div></div>
          ))}
        </article>
        <aside className="panel">
          <h3 className="title">Guardrails in the product</h3>
          <p className="desc">The interface preserves the boundaries of the current evidence.</p>
          <div className="status"><small>Periods and directions</small><b>Never silently aggregated</b></div>
          <div className="status"><small>Criterion weights</small><b>Explicit and user supplied</b></div>
          <div className="status"><small>Research conclusions</small><b>Not implied by a model run</b></div>
        </aside>
      </section>

      <section className="panel overview-register">
        <div className="section-heading"><div><p className="eyebrow">At a glance</p><h3 className="title">What this workspace contains</h3></div><span className="tag">Research-aware interface</span></div>
        <div className="table-wrap"><table className="data-table"><thead><tr><th>Area</th><th>Current state</th><th>How to use it</th></tr></thead><tbody>{overviewRows.map(([area, state, guidance]) => <tr key={area}><td><b>{area}</b></td><td>{state}</td><td>{guidance}</td></tr>)}</tbody></table></div>
      </section>
    </AppShell>
  );
}
