import type { DemoRun, RunSummary } from './types'

// Data for the demo screens. Real runs come from the API (GET /api/demo/runs[/<id>]).
// If the API is unreachable, or the URL has ?fixture, the committed sample run is used and the
// screens show a "sample data" badge.

export interface Loaded<T> {
  data: T
  sample: boolean
}

export class NotFoundError extends Error {}

export function fixtureForced(): boolean {
  // in the query before the hash (/?fixture#/runs/...), so it survives hash navigation
  return new URLSearchParams(window.location.search).has('fixture')
}

let sampleRun: Promise<DemoRun> | null = null

function loadSample(): Promise<DemoRun> {
  // dynamic import keeps the sample out of the main bundle
  sampleRun ??= import('./fixtures/demo-run.sample.json').then((m) => m.default as unknown as DemoRun)
  return sampleRun
}

function summarize(run: DemoRun): RunSummary {
  const { id, project, created_at, commit, counts } = run
  return { id, project, created_at, commit, counts }
}

async function getJson<T>(url: string): Promise<T> {
  const r = await fetch(url, { headers: { Accept: 'application/json' } })
  if (r.status === 404) throw new NotFoundError(url)
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`)
  const type = r.headers.get('content-type') ?? ''
  if (!type.includes('json')) throw new Error(`not JSON: ${type}`)
  return (await r.json()) as T
}

export async function listRuns(): Promise<Loaded<RunSummary[]>> {
  if (!fixtureForced()) {
    try {
      return { data: await getJson<RunSummary[]>('/api/demo/runs'), sample: false }
    } catch {
      // API down or without the demo endpoints: fall back to the sample
    }
  }
  return { data: [summarize(await loadSample())], sample: true }
}

export async function getRun(id: string): Promise<Loaded<DemoRun>> {
  const sample = fixtureForced() ? await loadSample() : null
  if (sample) {
    if (sample.id !== id) throw new NotFoundError(id)
    return { data: sample, sample: true }
  }
  try {
    return { data: await getJson<DemoRun>(`/api/demo/runs/${encodeURIComponent(id)}`), sample: false }
  } catch (e) {
    const fallback = await loadSample()
    if (fallback.id === id) return { data: fallback, sample: true }
    throw e
  }
}
