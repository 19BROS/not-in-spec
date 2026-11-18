import { useMemo, useState } from 'react'
import { num } from '../format'
import type { DemoRun } from '../types'
import { Card } from '../ui'

export function Symbols(props: { run: DemoRun }) {
  const symbols = props.run.symbols
  const [q, setQ] = useState('')
  const [kind, setKind] = useState('')
  const kinds = useMemo(() => [...new Set(symbols.map((s) => s.kind))].sort(), [symbols])

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase()
    return symbols.filter(
      (s) =>
        (!kind || s.kind === kind) &&
        (!needle ||
          s.path.toLowerCase().includes(needle) ||
          s.parameters.some((p) => p.toLowerCase().includes(needle))),
    )
  }, [symbols, q, kind])

  return (
    <>
      <div className="page-head">
        <h1>Symbols</h1>
        <p className="muted">
          The inventory built by code from the Sphinx build: {num(props.run.counts.symbols)} symbols,{' '}
          {num(props.run.counts.parameters)} parameters.
        </p>
      </div>
      <div className="filters card">
        <label>
          <span className="label">Kind</span>
          <select value={kind} onChange={(e) => setKind(e.target.value)}>
            <option value="">All</option>
            {kinds.map((k) => (
              <option key={k} value={k}>
                {k}
              </option>
            ))}
          </select>
        </label>
        <label className="grow">
          <span className="label">Search</span>
          <input type="search" value={q} placeholder="path or parameter" onChange={(e) => setQ(e.target.value)} />
        </label>
      </div>
      <Card
        title={`${num(filtered.length)} symbol${filtered.length === 1 ? '' : 's'}`}
        sub={
          symbols.length < props.run.counts.symbols
            ? `This run file holds ${num(symbols.length)} of the ${num(props.run.counts.symbols)} symbols (trimmed sample).`
            : undefined
        }
        flush
      >
        <table className="table">
          <thead>
            <tr>
              <th>Path</th>
              <th>Kind</th>
              <th>Parameters</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((s, i) => (
              <tr key={`${s.path}:${i}`}>
                <td className="mono">{s.path}</td>
                <td>{s.kind}</td>
                <td className="mono small">{s.parameters.length ? s.parameters.join(', ') : <span className="muted">–</span>}</td>
                <td className="mono small muted">{s.source ?? '–'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </>
  )
}
