import { useEffect, useState } from 'react'
import { NotFoundError, getRun, listRuns, type Loaded } from './api'
import { runHref } from './format'
import { Claims } from './screens/Claims'
import { RunDashboard } from './screens/RunDashboard'
import { Runs } from './screens/Runs'
import { Symbols } from './screens/Symbols'
import type { DemoRun, RunSummary } from './types'
import { Layout, Message, type NavItem } from './ui'

// Tiny hash router (no dependency):
//   #/                     runs list
//   #/runs/<id>            run dashboard
//   #/runs/<id>/claims     claims (+ ?status=&extractor=&source=&q=&claim=)
//   #/runs/<id>/symbols    symbols

type RunPage = 'run' | 'claims' | 'symbols'
type Route =
  | { page: 'runs' }
  | { page: RunPage; id: string; query: URLSearchParams; qs: string }
  | { page: 'notfound' }

function parseHash(hash: string): Route {
  const raw = hash.replace(/^#/, '') || '/'
  const at = raw.indexOf('?')
  const path = at < 0 ? raw : raw.slice(0, at)
  const qs = at < 0 ? '' : raw.slice(at + 1)
  const parts = path.split('/').filter(Boolean)
  if (parts.length === 0) return { page: 'runs' }
  if (parts[0] === 'runs' && parts.length >= 2 && parts.length <= 3) {
    let id: string
    try {
      id = decodeURIComponent(parts[1])
    } catch {
      return { page: 'notfound' }
    }
    const sub = parts[2] ?? ''
    const page: RunPage | null = sub === '' ? 'run' : sub === 'claims' || sub === 'symbols' ? sub : null
    if (page) return { page, id, query: new URLSearchParams(qs), qs }
  }
  return { page: 'notfound' }
}

function useRoute(): Route {
  const [route, setRoute] = useState(() => parseHash(window.location.hash))
  useEffect(() => {
    const onChange = () => {
      setRoute(parseHash(window.location.hash))
      window.scrollTo(0, 0)
    }
    window.addEventListener('hashchange', onChange)
    return () => window.removeEventListener('hashchange', onChange)
  }, [])
  return route
}

type Async<T> = { key: string; data?: Loaded<T>; error?: unknown }

function errorText(e: unknown): string {
  return e instanceof Error ? e.message : String(e)
}

function App() {
  const route = useRoute()
  const runId = route.page === 'run' || route.page === 'claims' || route.page === 'symbols' ? route.id : null
  const onRuns = route.page === 'runs'

  const [runs, setRuns] = useState<Async<RunSummary[]> | null>(null)
  const [run, setRun] = useState<Async<DemoRun> | null>(null)

  // the list is reloaded every time it is opened, so a new CLI run shows up
  useEffect(() => {
    if (!onRuns) return
    let live = true
    listRuns().then(
      (data) => live && setRuns({ key: 'runs', data }),
      (error: unknown) => live && setRuns({ key: 'runs', error }),
    )
    return () => {
      live = false
    }
  }, [onRuns])

  useEffect(() => {
    if (!runId) return
    let live = true
    getRun(runId).then(
      (data) => live && setRun({ key: runId, data }),
      (error: unknown) => live && setRun({ key: runId, error }),
    )
    return () => {
      live = false
    }
  }, [runId])

  const current = runId && run?.key === runId ? run : null
  const loaded = current?.data?.data ?? null

  useEffect(() => {
    document.title = loaded ? `${loaded.project} · NOT-IN-SPEC` : 'NOT-IN-SPEC'
  }, [loaded])

  const nav: NavItem[] = [{ label: 'Runs', href: '#/', active: onRuns }]
  if (runId) {
    nav.push(
      { label: loaded?.project ?? 'Run', href: '', active: false },
      { label: 'Dashboard', href: runHref(runId), active: route.page === 'run' },
      { label: 'Claims', href: runHref(runId, 'claims'), active: route.page === 'claims' },
      { label: 'Symbols', href: runHref(runId, 'symbols'), active: route.page === 'symbols' },
    )
  }

  const pageName = route.page === 'claims' ? 'Claims' : route.page === 'symbols' ? 'Symbols' : null
  const crumbs = (
    <>
      <a href="#/">Runs</a>
      {runId && (
        <>
          <span className="sep">/</span>
          {pageName ? <a href={runHref(runId)}>{loaded?.project ?? runId}</a> : <span>{loaded?.project ?? runId}</span>}
        </>
      )}
      {pageName && (
        <>
          <span className="sep">/</span>
          <span>{pageName}</span>
        </>
      )}
    </>
  )

  let body
  let sample = false
  if (route.page === 'notfound') {
    body = (
      <Message title="Page not found">
        <a href="#/">Back to runs</a>
      </Message>
    )
  } else if (route.page === 'runs') {
    if (!runs) body = <p className="muted">Loading runs…</p>
    else if (runs.error || !runs.data) body = <Message title="Could not load runs">{errorText(runs.error)}</Message>
    else {
      sample = runs.data.sample
      body = <Runs runs={runs.data.data} />
    }
  } else if (!current) {
    body = <p className="muted">Loading run…</p>
  } else if (current.error || !current.data) {
    body =
      current.error instanceof NotFoundError ? (
        <Message title="Run not found">
          <p className="muted">
            No run <code>{runId}</code>. <a href="#/">Back to runs</a>
          </p>
        </Message>
      ) : (
        <Message title="Could not load the run">
          <p className="muted">
            {errorText(current.error)}. Is the API running (<code>uv run uvicorn notinspec_api.main:app</code> from the
            repo root)? The sample run is at <a href="?fixture#/">?fixture</a>.
          </p>
        </Message>
      )
  } else {
    sample = current.data.sample
    const data = current.data.data
    if (route.page === 'run') body = <RunDashboard run={data} />
    else if (route.page === 'claims') body = <Claims key={route.qs} run={data} query={route.query} />
    else body = <Symbols run={data} />
  }

  return (
    <Layout nav={nav} crumbs={crumbs} sample={sample}>
      {body}
    </Layout>
  )
}

export default App
