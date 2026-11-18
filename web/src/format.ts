import type { ClaimStatus, ClaimsBlock, StepStatus } from './types'

export type Tone = 'ok' | 'warn' | 'bad' | 'muted' | 'info'

export const STATUS_LABEL: Record<ClaimStatus, string> = {
  kept: 'kept',
  citation_not_found: 'citation not found',
  not_checkable: 'not checkable',
  nli_neutral: 'NLI neutral',
  nli_contradiction: 'NLI contradiction',
  id_missing: 'identifier missing',
}

export const STATUS_TONE: Record<ClaimStatus, Tone> = {
  kept: 'ok',
  citation_not_found: 'bad',
  not_checkable: 'muted',
  nli_neutral: 'warn',
  nli_contradiction: 'bad',
  id_missing: 'warn',
}

/** Why a claim was dropped (SPEC §6.4 grounding). */
export const STATUS_REASON: Record<ClaimStatus, string> = {
  kept: 'Citation found in prose, NLI entails the claim, and its section names every identifier in it.',
  citation_not_found: 'Dropped: the citation the extractor gave is not in the chunk text.',
  not_checkable:
    'Dropped: the citation is only outside prose (code block, table, signature or type), so NLI cannot check it.',
  nli_neutral: 'Dropped: NLI says the premise neither entails nor contradicts the claim.',
  nli_contradiction: 'Dropped: NLI says the premise contradicts the claim.',
  id_missing:
    'Dropped: NLI kept it, but the claim names identifiers, numbers or versions its section never names.',
}

export const STEP_TONE: Record<StepStatus, Tone> = {
  done: 'ok',
  failed: 'bad',
  skipped: 'muted',
  not_implemented: 'muted',
}

export const STEP_LABEL: Record<StepStatus, string> = {
  done: 'done',
  failed: 'failed',
  skipped: 'skipped',
  not_implemented: 'not built yet',
}

export function formatDate(iso: string): string {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function short(hash: string, n = 7): string {
  return hash ? hash.slice(0, n) : '–'
}

export function num(n: number | null | undefined): string {
  return n == null ? '–' : n.toLocaleString('en-US')
}

export function runHref(runId: string, page = ''): string {
  return `#/runs/${encodeURIComponent(runId)}${page ? `/${page}` : ''}`
}

export function claimsHref(runId: string, filters: Record<string, string> = {}): string {
  const q = new URLSearchParams(filters).toString()
  return `${runHref(runId, 'claims')}${q ? `?${q}` : ''}`
}

/** Total claims over all extractors and statuses (from counts, not items: items may be trimmed). */
export function claimTotals(block: ClaimsBlock): number {
  return Object.values(block.counts).reduce(
    (sum, byStatus) => sum + Object.values(byStatus).reduce((a, b) => a + (b ?? 0), 0),
    0,
  )
}
