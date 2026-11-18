// Contract: run.json v0 (docs/plans/demo-cli-web.md). Field names are binding for core and web.

export type StepId = 'read' | 'inventory' | 'claims' | 'grounding' | 'tests' | 'models' | 'evaluate'
export type StepStatus = 'done' | 'skipped' | 'failed' | 'not_implemented'

export interface Step {
  id: StepId
  label: string
  status: StepStatus
  detail?: string
}

export interface RunCounts {
  files: number
  chunks: number
  symbols: number
  parameters: number
  changes: number
  warnings: number
  claims: number | null
  claims_kept: number | null
}

export interface DocumentRow {
  source: string
  chunks: number
  tokens: number
  symbols: number
  claims: number
  claims_kept: number
}

export interface SymbolRow {
  path: string
  kind: string
  source: string | null
  parameters: string[]
}

export interface Change {
  symbol: string
  kind: string
  version: string | null
  parameter: string | null
  replacement: string | null
}

export const CLAIM_STATUSES = [
  'kept',
  'citation_not_found',
  'not_checkable',
  'nli_neutral',
  'nli_contradiction',
  'id_missing',
] as const
export type ClaimStatus = (typeof CLAIM_STATUSES)[number]

export interface NliScores {
  entailment: number
  neutral: number
  contradiction: number
  truncated: boolean
}

export interface Claim {
  id: string
  extractor: string
  source: string
  breadcrumb: string
  chunk_id: string
  type: string
  text: string
  citation: string
  status: ClaimStatus
  premise: string | null
  nli: NliScores | null
  missing: string[]
}

export interface ClaimsBlock {
  sources: string[]
  extractors: string[]
  counts: Record<string, Partial<Record<ClaimStatus, number>>>
  versions: Record<string, unknown>
  items: Claim[]
}

export interface DemoRun {
  schema: 'notinspec-demo-run'
  schema_version: 0
  id: string
  project: string
  created_at: string
  commit: string
  tool_version: string
  docs: { sphinx_version: string | null; input_hash: string; config_hash: string }
  counts: RunCounts
  steps: Step[]
  documents: DocumentRow[]
  symbols: SymbolRow[]
  changes: Change[]
  warnings: string[]
  claims: ClaimsBlock | null
}

/** One row of GET /api/demo/runs. */
export interface RunSummary {
  id: string
  project: string
  created_at: string
  commit: string
  counts: RunCounts
}
