import type { ReactNode } from 'react'
import type { Tone } from './format'

export interface NavItem {
  label: string
  href: string
  active: boolean
  indent?: boolean
}

export function Layout(props: {
  nav: NavItem[]
  crumbs: ReactNode
  sample: boolean
  children: ReactNode
}) {
  return (
    <div className="shell">
      <aside className="sidebar">
        <a className="logo" href="#/">
          <span className="logo-mark">n</span>
          <span className="logo-text">not-in-spec</span>
        </a>
        <nav>
          {props.nav.map((n) =>
            n.href === '' ? (
              <div key={`h:${n.label}`} className="nav-heading">
                {n.label}
              </div>
            ) : (
            <a
              key={n.href}
              href={n.href}
              className={`nav-item${n.active ? ' active' : ''}${n.indent ? ' indent' : ''}`}
            >
              {n.label}
            </a>
            ),
          )}
        </nav>
      </aside>
      <div className="main">
        <header className="topbar">
          <div className="crumbs">{props.crumbs}</div>
          {props.sample && (
            <span className="pill tone-info" title="The API is unreachable or the URL has ?fixture">
              sample data
            </span>
          )}
        </header>
        <main className="content">{props.children}</main>
      </div>
    </div>
  )
}

export function Card(props: { title?: ReactNode; sub?: ReactNode; action?: ReactNode; children: ReactNode; flush?: boolean }) {
  return (
    <section className="card">
      {(props.title || props.action) && (
        <div className="card-head">
          <div>
            {props.title && <h2 className="card-title">{props.title}</h2>}
            {props.sub && <p className="card-sub">{props.sub}</p>}
          </div>
          {props.action}
        </div>
      )}
      <div className={props.flush ? 'card-body flush' : 'card-body'}>{props.children}</div>
    </section>
  )
}

export function Stat(props: { label: string; value: string; sub?: string }) {
  return (
    <div className="card stat">
      <div className="label">{props.label}</div>
      <div className="stat-value">{props.value}</div>
      {props.sub && <div className="stat-sub">{props.sub}</div>}
    </div>
  )
}

export function Pill(props: { tone: Tone; children: ReactNode }) {
  return <span className={`pill tone-${props.tone}`}>{props.children}</span>
}

export function Bar(props: { value: number; max: number; tone?: Tone | 'accent' }) {
  const pct = props.max > 0 ? Math.max(0, Math.min(100, (props.value / props.max) * 100)) : 0
  return (
    <div className="bar">
      <div className={`bar-fill fill-${props.tone ?? 'accent'}`} style={{ width: `${pct}%` }} />
    </div>
  )
}

export function Message(props: { title: string; children?: ReactNode }) {
  return (
    <div className="card message">
      <h2>{props.title}</h2>
      {props.children}
    </div>
  )
}
