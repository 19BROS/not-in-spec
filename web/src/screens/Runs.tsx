import { formatDate, num, short } from '../format'
import type { RunSummary } from '../types'
import { Card } from '../ui'

const CLI = `uv run notinspec demo --config core/examples/sphinx/trio/notinspec.yaml --no-claims`

export function Runs(props: { runs: RunSummary[] }) {
  return (
    <>
      <div className="page-head">
        <h1>Runs</h1>
        <p className="muted">
          Each run is one <code>notinspec demo</code> on a project's docs: ingestion, inventory and claims with
          grounding. Newest first.
        </p>
      </div>
      <Card flush>
        {props.runs.length === 0 ? (
          <div className="empty">
            <p>No runs yet. Make one from the repo root:</p>
            <pre className="code">{CLI}</pre>
            <p className="muted">Then refresh this page. Runs are read from <code>tmp/runs/</code>.</p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Project</th>
                <th>Date</th>
                <th>Commit</th>
                <th className="num">Files</th>
                <th className="num">Chunks</th>
                <th className="num">Symbols</th>
                <th className="num">Claims kept / claims</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {props.runs.map((r) => {
                const href = `#/runs/${encodeURIComponent(r.id)}`
                return (
                  <tr key={r.id} className="clickable" onClick={() => (window.location.hash = href.slice(1))}>
                    <td>
                      <a href={href} className="strong">
                        {r.project}
                      </a>
                      <div className="mono small muted">{r.id}</div>
                    </td>
                    <td>{formatDate(r.created_at)}</td>
                    <td className="mono">{short(r.commit)}</td>
                    <td className="num">{num(r.counts.files)}</td>
                    <td className="num">{num(r.counts.chunks)}</td>
                    <td className="num">{num(r.counts.symbols)}</td>
                    <td className="num">
                      {r.counts.claims == null ? '–' : `${num(r.counts.claims_kept)} / ${num(r.counts.claims)}`}
                    </td>
                    <td className="num">
                      <a href={href}>Open</a>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        )}
      </Card>
    </>
  )
}
