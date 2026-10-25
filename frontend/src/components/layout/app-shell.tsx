"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Icon } from "@/components/ui/icons";
import { ThemeToggle } from "./theme-toggle";

const items = [
  ["Overview", "/", "activity"],
  ["Intersections", "/intersections", "map"],
  ["Decision Engine", "/decision-engine", "sliders"],
  ["Priority Rankings", "/priority-rankings", "ranking"],
  ["Time Analysis", "/time-analysis", "clock"],
  ["Sensitivity Analysis", "/sensitivity-analysis", "chart"],
  ["Methodology", "/methodology", "book"],
] as const;

type AppShellProps = {
  children: React.ReactNode;
  title: string;
  path: string;
};

export function AppShell({ children, title, path }: AppShellProps) {
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("mobilityforge-sidebar") === "collapsed";
    const frame = requestAnimationFrame(() => setCollapsed(stored));
    return () => cancelAnimationFrame(frame);
  }, []);

  function toggleSidebar() {
    const next = !collapsed;
    setCollapsed(next);
    localStorage.setItem("mobilityforge-sidebar", next ? "collapsed" : "expanded");
  }

  return (
    <div className="shell" data-sidebar-collapsed={collapsed}>
      <aside className="side" aria-label="MobilityForge workspace">
        <div className="side-brand-row">
          <Link className="brand" href="/" aria-label="MobilityForge overview">
            <span className="mark"><Icon name="route" size={19} /></span>
            <span className="brand-wordmark">Mobility<em>Forge</em></span>
          </Link>
          <button
            className="sidebar-toggle"
            type="button"
            onClick={toggleSidebar}
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
            aria-expanded={!collapsed}
          >
            <Icon name={collapsed ? "chevron-right" : "chevron-left"} size={16} />
          </button>
        </div>

        <p className="nav-label">Workspace</p>
        <nav aria-label="Primary navigation">
          <ul className="nav">
            {items.map(([label, href, icon]) => (
              <li key={href}>
                <Link className="link" data-active={path === href} href={href} title={collapsed ? label : undefined}>
                  <Icon name={icon} size={17} />
                  <span>{label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div className="side-note">
          <span className="side-note-dot" />
          <div><b>Urban Mobility Intelligence</b>Building Better Mobility Systems.</div>
        </div>
      </aside>

      <main className="main-area">
        <header className="top">
          <div className="page-context">
            <span className="page-context-label">MobilityForge</span>
            <h1>{title}</h1>
          </div>
          <ThemeToggle />
        </header>
        <nav className="mobile" aria-label="Mobile navigation">
          {items.map(([label, href]) => <Link key={href} data-active={path === href} href={href}>{label}</Link>)}
        </nav>
        <div className="content">{children}</div>
      </main>
    </div>
  );
}
