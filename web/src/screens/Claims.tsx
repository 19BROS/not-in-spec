import { useMemo, useState } from 'react'
import { STATUS_LABEL, STATUS_REASON, STATUS_TONE, claimTotals, num, runHref } from '../format'
import { CLAIM_STATUSES, type Claim, type ClaimsBlock, type DemoRun, type NliScores } from '../types'
import { Bar, Card, Message, Pill } from '../ui'

interface Filters {
  status: string // '' | 'dropped' | ClaimStatus
  extractor: string
  source: string
  q: string
}

const FILTER_KEYS = ['status', 'extractor', 'source', 'q'] as const

export function Claims(props: { run: DemoRun; query: URLSearchParams }) {
  const block = props.run.claims
  if (!block) {
    return (
      <Message title="No claims in this run">
        <p className="muted">
          This run was made with <code>--no-claims</code>. See the <a href={runHref(props.run.id)}>dashboard</a> for
          ingestion and inventory.
        </p>
      </Message>
    )
  }
  return <ClaimsView run={props.run} block={block} query={props.query} />
}

function ClaimsView(props: { run: DemoRun; block: ClaimsBlock; query: URLSearchParams }) {
  const { block } = props
  const [filters, setFilters] = useState<Filters>(() => ({
    status: props.query.get('status') ?? '',
    extractor: props.query.get('extractor') ?? '',
    source: props.query.get('source') ?? '',
    q: props.query.get('q') ?? '',
  }))
  const [selectedId, setSelectedId] = useState<string | null>(props.query.get('claim'))

  // keep filters and selection in the URL (replaceState: no history entry per keystroke)
  const sync = (f: Filters, claim: string | null) => {
    const q = new URLSearchParams()
    for (const k of FILTER_KEYS) if (f[k]) q.set(k, f[k])
    if (claim) q.set('claim', claim)
    const s = q.toString()
    window.history.replaceState(null, '', `${runHref(props.run.id, 'claims')}${s ? `?${s}` : ''}`)
  }
  const setFilter = (k: keyof Filters, v: string) => {
    const f = { ...filters, [k]: v }
    setFilters(f)
    sync(f, selectedId)
  }
  const select = (id: string) => {
    setSelectedId(id)
    sync(filters, id)
  }

  const items = block.items
  const statusCounts = useMemo(() => {
    const m = new Map<string, number>()
    for (const c of items) m.set(c.status, (m.get(c.status) ?? 0) + 1)
    return m
  }, [items])

  const filtered = useMemo(() => {
    const q = filters.q.trim().toLowerCase()
    return items.filter(
      (c) =>
        (!filters.status ||
          (filters.status === 'dropped' ? c.status !== 'kept' : c.status === filters.status)) &&
        (!filters.extractor || c.extractor === filters.extractor) &&
        (!filters.source || c.source === filters.source) &&
        (!q ||
          c.text.toLowerCase().includes(q) ||
          c.citation.toLowerCase().includes(q) ||
          c.breadcrumb.toLowerCase().includes(q)),
    )
  }, [items, filters])

  const selected = items.find((c) => c.id === selectedId) ?? filtered[0] ?? null
  const total = claimTotals(block)
  const dropped = items.length - (statusCounts.get('kept') ?? 0)
  const many = block.extractors.length > 1

  return (
    <>
      <div className="page-head">
        <h1>Claims</h1>
        <p className="muted">
          Atomic claims extracted from the docs, each with a citation, then grounded: citation check, NLI against
          the premise, identifier check. Dropped claims show why. Select one to see the details.
        </p>
      </div>

      <div className="filters card">
        <label>
          <span className="label">Status</span>
          <select value={filters.status} onChange={(e) => setFilter('status', e.target.value)}>
            <option value="">All ({num(items.length)})</option>
            <option value="dropped">Dropped, any reason ({num(dropped)})</option>
            {CLAIM_STATUSES.map((s) => (
              <option key={s} value={s}>
                {STATUS_LABEL[s]} ({num(statusCounts.get(s) ?? 0)})
              </option>
            ))}
          </select>
        </label>
        <label>
          <span className="label">Extractor</span>
          <select value={filters.extractor} onChange={(e) => setFilter('extractor', e.target.value)}>
            <option value="">All</option>
            {block.extractors.map((x) => (
              <option key={x} value={x}>
                {x}
              </option>
            ))}
          </select>
        </label>
        <label>
          <span className="label">Source</span>
          <select value={filters.source} onChange={(e) => setFilter('source', e.target.value)}>
            <option value="">All</option>
            {block.sources.map((x) => (
              <option key={x} value={x}>
                {x}
              </option>
            ))}
          </select>
        </label>
        <label className="grow">
          <span className="label">Search</span>
          <input
            type="search"
            value={filters.q}
            placeholder="claim, citation or section"
            onChange={(e) => setFilter('q', e.target.value)}
          />
        </label>
      </div>

      <div className="split">
        <Card
          title={`${num(filtered.length)} claim${filtered.length === 1 ? '' : 's'}`}
          sub={
            items.length < total
              ? `This run file holds ${num(items.length)} of the ${num(total)} claims (trimmed sample).`
              : `of ${num(items.length)} in this run`
          }
          flush
        >
          {filtered.length === 0 ? (
            <p className="muted pad">No claims match these filters.</p>
          ) : (
            <table className="table claims-table">
              <thead>
                <tr>
                  <th>Status</th>
                  <th>Where</th>
                  <th>Claim</th>
                  {many && <th>Extractor</th>}
                </tr>
              </thead>
              <tbody>
                {filtered.map((c) => (
                  <tr
                    key={c.id}
                    className={`clickable${selected?.id === c.id ? ' selected' : ''}`}
                    tabIndex={0}
                    onClick={() => select(c.id)}
                    onKeyDown={(e) => e.key === 'Enter' && select(c.id)}
                  >
                    <td>
                      <Pill tone={STATUS_TONE[c.status]}>{STATUS_LABEL[c.status]}</Pill>
                    </td>
                    <td className="where">
                      <div className="mono small">{c.source}</div>
                      <div className="small muted">{lastCrumb(c.breadcrumb)}</div>
                    </td>
                    <td>
                      <div className="claim-text">{c.text}</div>
                    </td>
                    {many && <td className="mono small">{c.extractor}</td>}
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Card>
        <div className="detail">{selected && <ClaimDetail claim={selected} />}</div>
      </div>
    </>
  )
}

function lastCrumb(b: string): string {
  const parts = b.split(' > ')
  return parts.slice(-2).join(' › ')
}

function ClaimDetail(props: { claim: Claim }) {
  const c = props.claim
  return (
    <Card title="Claim detail" sub={c.extractor}>
      <div className="detail-status">
        <Pill tone={STATUS_TONE[c.status]}>{STATUS_LABEL[c.status]}</Pill>
        <span className="small muted">{c.type}</span>
      </div>
      <p className="small">{STATUS_REASON[c.status]}</p>

      <h3 className="label">Claim</h3>
      <p className="claim-big">{c.text}</p>

      <h3 className="label">Citation (quoted by the extractor)</h3>
      <pre className="code">{c.citation}</pre>

      <h3 className="label">NLI premise</h3>
      {c.premise ? (
        <p className="premise">{c.premise}</p>
      ) : (
        <p className="small muted">
          None: {c.status === 'citation_not_found' ? 'the citation is not in the chunk' : 'the citation is not in prose'}
          , so NLI did not run.
        </p>
      )}

      {c.nli && (
        <>
          <h3 className="label">NLI (premise ⇒ claim)</h3>
          <NliBars nli={c.nli} />
        </>
      )}

      {(c.missing.length > 0 || c.nli) && (
        <>
          <h3 className="label">Identifiers not named in the section</h3>
          {c.missing.length === 0 ? (
            <p className="small muted">None.</p>
          ) : (
            <div className="chips">
              {c.missing.map((m) => (
                <code key={m} className="chip">
                  {m}
                </code>
              ))}
            </div>
          )}
        </>
      )}

      <h3 className="label">Where</h3>
      <p className="small">{c.breadcrumb}</p>
      <p className="small muted mono">
        {c.source} · chunk {c.chunk_id}
      </p>
    </Card>
  )
}

function NliBars(props: { nli: NliScores }) {
  const rows: [keyof Omit<NliScores, 'truncated'>, 'ok' | 'muted' | 'bad'][] = [
    ['entailment', 'ok'],
    ['neutral', 'muted'],
    ['contradiction', 'bad'],
  ]
  const top = rows.reduce((a, b) => (props.nli[b[0]] > props.nli[a[0]] ? b : a))[0]
  return (
    <div className="nli">
      {rows.map(([k, tone]) => (
        <div key={k} className={`bar-row${k === top ? ' top' : ''}`}>
          <span className="bar-label">{k}</span>
          <Bar value={props.nli[k]} max={1} tone={tone} />
          <span className="bar-count">{props.nli[k].toFixed(2)}</span>
        </div>
      ))}
      {props.nli.truncated && <p className="small muted">The premise was cut to fit the NLI model.</p>}
    </div>
  )
}
