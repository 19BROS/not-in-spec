import { STATUS_LABEL, STATUS_TONE, STEP_LABEL, STEP_TONE, claimsHref, formatDate, num, short } from '../format'
import { CLAIM_STATUSES, type DemoRun, type Step } from '../types'
import { Bar, Card, Pill, Stat } from '../ui'

export function RunDashboard(props: { run: DemoRun }) {
  const { run } = props
  const c = run.counts
  const meta = [
    formatDate(run.created_at),
    run.commit ? `commit ${short(run.commit)}` : null,
    run.docs.sphinx_version ? `Sphinx ${run.docs.sphinx_version}` : null,
    `input ${short(run.docs.input_hash, 8)}`,
    `notinspec ${run.tool_version}`,
  ].filter(Boolean)

  return (
    <>
      <div className="page-head">
        <h1>{run.project} docs</h1>
        <p className="muted">{meta.join(' · ')}</p>
      </div>

      {run.warnings.length > 0 && (
        <div className="banner warn">
          {run.warnings.length} ingestion warning{run.warnings.length === 1 ? '' : 's'}: see the list below.
        </div>
      )}

      <div className="stats">
        <Stat label="Files" value={num(c.files)} />
        <Stat label="Chunks" value={num(c.chunks)} />
        <Stat label="Symbols" value={num(c.symbols)} />
        <Stat label="Parameters" value={num(c.parameters)} />
        <Stat label="Changes" value={num(c.changes)} sub="version directives" />
        <Stat
          label="Claims kept"
          value={num(c.claims_kept)}
          sub={c.claims == null ? 'claims not run' : `of ${num(c.claims)} extracted`}
        />
      </div>

      <div className="grid-2">
        <Pipeline steps={run.steps} />
        <ClaimsByStatus run={run} />
      </div>

      <div className="grid-2 wide-left">
        <Documents run={run} />
        <div className="stack">
          <Changes run={run} />
          {run.warnings.length > 0 && (
            <Card title="Warnings" sub="From ingestion">
              <ul className="plain-list">
                {run.warnings.map((w, i) => (
                  <li key={i} className="small">
                    {w}
                  </li>
                ))}
              </ul>
            </Card>
          )}
        </div>
      </div>
    </>
  )
}

function StepIcon(props: { step: Step }) {
  const s = props.step.status
  if (s === 'done') return <span className="step-icon done">✓</span>
  if (s === 'failed') return <span className="step-icon failed">✕</span>
  return <span className="step-icon idle" />
}

function Pipeline(props: { steps: Step[] }) {
  const done = props.steps.filter((s) => s.status === 'done').length
  return (
    <Card title="Pipeline" sub={`${done} of ${props.steps.length} steps done in this run`}>
      <Bar value={done} max={props.steps.length} />
      <ol className="steps">
        {props.steps.map((s) => (
          <li key={s.id} className={`step ${s.status}`}>
            <StepIcon step={s} />
            <div className="step-text">
              <div className="step-label">
                {s.label}
                {s.status !== 'done' && <Pill tone={STEP_TONE[s.status]}>{STEP_LABEL[s.status]}</Pill>}
              </div>
              {s.detail && <div className="small muted">{s.detail}</div>}
            </div>
          </li>
        ))}
      </ol>
    </Card>
  )
}

function ClaimsByStatus(props: { run: DemoRun }) {
  const block = props.run.claims
  if (!block) {
    return (
      <Card title="Claims by status">
        <p className="muted">
          Claims were not run for this run (<code>--no-claims</code>).
        </p>
      </Card>
    )
  }
  return (
    <Card
      title="Claims by status"
      sub={`Per extractor · pages: ${block.sources.join(', ')}`}
      action={<a href={claimsHref(props.run.id)}>All claims →</a>}
    >
      {block.extractors.map((ex) => {
        const counts = block.counts[ex] ?? {}
        const total = CLAIM_STATUSES.reduce((a, s) => a + (counts[s] ?? 0), 0)
        return (
          <div key={ex} className="extractor">
            <div className="extractor-head">
              <span className="mono">{ex}</span>
              <span className="muted small">{num(total)} claims</span>
            </div>
            {CLAIM_STATUSES.map((s) => (
              <a key={s} className="bar-row" href={claimsHref(props.run.id, { status: s, extractor: ex })}>
                <span className="bar-label">{STATUS_LABEL[s]}</span>
                <Bar value={counts[s] ?? 0} max={total} tone={s === 'kept' ? 'accent' : STATUS_TONE[s]} />
                <span className="bar-count">{num(counts[s] ?? 0)}</span>
              </a>
            ))}
          </div>
        )
      })}
    </Card>
  )
}

function Documents(props: { run: DemoRun }) {
  const ran = new Set(props.run.claims?.sources ?? [])
  return (
    <Card title="Documents" sub="Pages read from the Sphinx build" flush>
      <table className="table">
        <thead>
          <tr>
            <th>Source</th>
            <th className="num">Chunks</th>
            <th className="num">Tokens</th>
            <th className="num">Symbols</th>
            <th className="num">Claims</th>
            <th className="num">Kept</th>
          </tr>
        </thead>
        <tbody>
          {props.run.documents.map((d) => (
            <tr key={d.source}>
              <td className="mono">
                {ran.has(d.source) ? (
                  <a href={claimsHref(props.run.id, { source: d.source })}>{d.source}</a>
                ) : (
                  d.source
                )}
              </td>
              <td className="num">{num(d.chunks)}</td>
              <td className="num">{num(d.tokens)}</td>
              <td className="num">{num(d.symbols)}</td>
              <td className="num">{ran.has(d.source) ? num(d.claims) : <span className="muted">–</span>}</td>
              <td className="num">{ran.has(d.source) ? num(d.claims_kept) : <span className="muted">–</span>}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  )
}

function Changes(props: { run: DemoRun }) {
  const changes = props.run.changes
  return (
    <Card title="Changes" sub="Version directives in the docs (deprecated, removed, …)" flush>
      {changes.length === 0 ? (
        <p className="muted pad">No changes found.</p>
      ) : (
        <ul className="change-list">
          {changes.map((ch, i) => (
            <li key={i}>
              <div className="mono small">
                {ch.symbol}
                {ch.parameter && <span className="muted">({ch.parameter})</span>}
              </div>
              <div className="small muted">
                <Pill tone={ch.kind === 'removed' ? 'bad' : 'warn'}>{ch.kind}</Pill>
                {ch.version && <> in {ch.version}</>}
                {ch.replacement && (
                  <>
                    {' '}
                    → use <span className="mono">{ch.replacement}</span>
                  </>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </Card>
  )
}
