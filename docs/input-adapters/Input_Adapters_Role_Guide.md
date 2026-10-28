# NOT-IN-SPEC: Role 2, Input adapters

Oct 27, 2026 · @RadoMuntag

Detailed working documentation for the **input adapters** role: what this part of the system does, how each step works, which technologies it uses, and what it hands to the other roles. It follows SPEC.md and FAQ.md. Where this document and SPEC disagree, SPEC wins and this document gets fixed.

Like the FAQ, most sections have three parts:

- **How it works**: the technical detail.
- **Example**: a concrete case, using the made-up **Acme Payments** API.
- **In plain words**: the same idea for someone who doesn't write code.

## 1. What the role owns

**How it works.** The adapters turn raw input (OpenAPI files and their git history) into the structured material every later stage works from. Per SPEC §2.1 and §11, this role owns:

| Deliverable | Used by |
| --- | --- |
| OpenAPI 3.x adapter: spec → operations, claims, snippets | generator (1), retrieval (4) |
| Version history: old spec versions taken from git | everyone downstream |
| Change claims (`removed`, `renamed`) from oasdiff | generator (1) |
| Spec files per version, ready for Prism | runner & verification (3) |
| Name index across all versions | failure causes (3) |

Adapters never call a language model and never decide whether an answer is right. They only describe *what the spec says*.

**In plain words.** I'm the one who reads the manual carefully, lists every fact in it, and keeps every old edition on the shelf. Everyone else in the team works from my lists.

## 2. Where it sits in the pipeline

```
 git repos ──► fetch ──► spec versions ──► load + normalize ──► claims ───► generator ──► …
 (Stripe,                     │                    │             snippets ─► retrieval (BM25)
  GitHub,                     │                    │
  Twilio)                     └──► oasdiff ──► removed / renamed claims
                              └──► name index ──► failure causes (runner)
                              └──► spec files ──► Prism (runner)
```

Everything lives inside the `core` package (`notinspec.adapters`). The CLI, worker and GitHub Action only call it.

## 3. Inputs: the three target APIs

**How it works.** All three targets publish official OpenAPI specs in public git repos (SPEC §4). Each target is described in a small config file, so adding a new API means adding config, not code.

```yaml
# targets/acme.yaml
id: acme
name: Acme Payments
repo: https://github.com/acme/openapi
spec_paths: [openapi/spec.yaml]     # one or more files
version_rule: monthly               # how history is sampled, see §5
history_from: 2024-11               # fixed first month of history, see §5
body_media_types: [application/json, application/x-www-form-urlencoded]
```

Things to know about the real targets (verify against the repos before relying on them):

| Target | Repo | Notes |
| --- | --- | --- |
| Stripe | `stripe/openapi` | One large spec. Request bodies are **form-encoded**, not JSON. Heavy use of `anyOf` and recursive `$ref`s. |
| GitHub REST | `github/rest-api-description` | Very large file (many MB). Several variants (github.com, GHES versions); only the public github.com one is used. |
| Twilio | `twilio/twilio-oai` | Split into **many files, one per product**. I pick a fixed subset (e.g. the core REST API) and record which files. Each file is a separate spec, and Prism mocks one spec at a time, so role 3 needs to know which file a claim came from (it's in `source`). Merging files vs. one Prism per file is to be agreed with role 3. |

**In plain words.** Each company keeps its blueprint in a public folder with every past edition. I write down where that folder is and which files in it I read.

## 4. Output contract

The output shapes are the contract with the rest of the team (roadmap week 8). They live in `core/src/notinspec/model.py` and are agreed with roles 1, 3 and 5. Any change goes through the lead.

**How it works.** Pydantic v2 models, frozen (immutable), serialized as canonical JSON.

```python
class SpecVersion(BaseModel):
    target: str  # "acme"
    version: str  # "2025-03" (our label, see §5)
    commit: str  # git commit SHA it came from
    committed_at: datetime
    files: list[str]  # paths of the spec files at that commit
    content_hash: str  # sha256 of the normalized content


class Operation(BaseModel):
    method: str  # "POST"
    path: str  # "/v1/charges"
    operation_id: str | None
    tags: list[str]
    deprecated: bool


class Claim(BaseModel):
    id: str  # stable, see below
    target: str
    layer: Literal["hard"]
    type: Literal[
        "endpoint-exists",
        "param-name",
        "required-field",
        "enum-value",
        "auth-scheme",
        "removed",
        "renamed",
    ]
    verify: Literal["execute-against-mock"]  # each claim carries its verification method
    operation: Operation | None  # None only for auth-scheme (one claim per scheme)
    location: Literal["path", "query", "header", "body"] | None
    name: str | None  # field or parameter name; scheme name for auth-scheme
    old_name: str | None  # only for renamed
    value_type: str | None  # "integer", "string", ...
    enum_values: list[str | int | float | bool] | None  # enums are not always strings
    example: Any | None  # example value from the spec, if any (for task templates)
    slice_key: str | None  # key of the tag slice holding the operation (full-sliced mode)
    since_version: str | None  # for removed / renamed: version where it changed
    fact: str  # human-readable sentence, for reports
    source: str  # JSON pointer into the spec
    spec_version: str


class Snippet(BaseModel):
    id: str
    target: str
    kind: Literal["operation", "tag"]
    key: str  # "POST /v1/charges" or tag name "Charges"
    text: str  # rendered, deterministic
    size_bytes: int
```

**Claim IDs** must be stable across runs, because the sampler, the run diff and the history all key on them. They extend the FAQ §2 format with the location, which is needed to tell a query parameter and a body field with the same name apart (the FAQ example will be updated to match). The shape depends on the type:

```
{target}/hard/{type}/{METHOD}-{path}                     endpoint-exists, removed (endpoint)
{target}/hard/{type}/{METHOD}-{path}/{location}/{name}   param-name, required-field, enum-value,
                                                         removed (field), renamed (new name)
{target}/hard/auth-scheme/{scheme}                       auth-scheme

acme/hard/endpoint-exists/POST-/v1/charges
acme/hard/required-field/POST-/v1/charges/body/amount
acme/hard/renamed/POST-/v1/charges/body/customer
acme/hard/auth-scheme/bearerAuth
```

Rules:

- The ID contains no spec version. A claim that exists in many versions keeps the same ID, which is what lets runs be compared week to week.
- Path placeholder names are blanked in IDs (`/v1/charges/{id}` → `/v1/charges/{}`), the same way the name index matches paths (§10). Otherwise a placeholder rename in the spec would change the ID without any real API change.
- IDs are opaque keys. Paths contain `/`, so nobody should split an ID to get its parts back; use the claim's fields.
- If the same change claim appears twice in history (a field removed, re-added, removed again), one claim is kept, with the **latest** `since_version`.

**In plain words.** The team agrees once on what a "fact" looks like on paper, so the roles after mine can rely on every fact having the same fields in the same places.

## 5. Step 1: fetching specs and history

**How it works.**

1. Clone each target repo once into a cache directory on the VM (`/data/repos/<target>`); later runs do `git fetch`.
2. List the commits that touched the spec files: `git log --format='%H %cI' -- openapi/spec.yaml`
3. Pick versions with a **fixed rule**, so the same history always yields the same versions. Default: the **last commit of each calendar month** that changed the spec, starting from the fixed month `history_from` in the target config. The window is never "the last N months" counted from today, because then the same repo would give different versions next month. The label is the month (`2025-03`). Targets with proper release tags can use `version_rule: tags` instead.
4. Export each chosen version's files with `git show <sha>:<path>` into `/data/specs/<target>/<version>/`.
5. The newest version is "current". Everything else is history.

Using the system `git` binary through `subprocess` keeps this simple and fast. Full clones of these repos are large, so the cache is kept between runs and never re-cloned.

**Example.** Acme's spec changed 41 times last year. The monthly rule turns that into 12 versions, `2024-11` … `2025-10`. The release that renamed `customer_id` landed in March, so it shows up as the step `2025-02 → 2025-03`.

**Known limit of the monthly rule.** One monthly step can bundle many changes. That makes more renames ambiguous, so the pairing rule (§9) turns them into plain `removed` claims, and a field that was added and removed within one month is never seen. Where a target has release tags (Stripe and Twilio publish them), `version_rule: tags` avoids most of this.

**In plain words.** Instead of every edition ever printed, I keep one edition per month. That's enough to see what changed and when, and it keeps the shelf a manageable size.

## 6. Step 2: loading and normalizing a spec

**How it works.**

1. **Parse.** JSON with `orjson`, YAML with PyYAML's C loader (`CSafeLoader`), which matters for GitHub's very large file.
2. **Validate.** `openapi-spec-validator` checks the file is valid OpenAPI 3.0/3.1. Problems are logged and counted, not fatal. Real specs are rarely perfect.
3. **Resolve `$ref`.** A small custom resolver, with a cycle guard (Stripe and others have recursive schemas). It remembers the original JSON pointer of each piece, which becomes the claim's `source`.
4. **Flatten operations.** For every `paths.<path>.<method>`: merge path-level and operation-level `parameters` (operation-level wins on the same `name` + `in`); take the request body for the configured media types (`application/json`, or form-encoded for Stripe); take effective security: operation-level `security` if present, otherwise the global one. An empty list (`security: []`) means no auth.
5. **Flatten schemas** into a list of body fields: `allOf` merges properties and `required` lists; for `oneOf` / `anyOf`, collect fields from all branches but mark a field as required **only if it is required in every branch**; skip `readOnly` properties (they appear in responses, not requests); go at most 2 levels deep, with nested fields using a dotted name (`shipping.address`).

The result is a list of normalized operations, each with its parameters, body fields, enums and security. Everything downstream works on this, never on raw YAML.

**Example.** Raw Acme fragment:

```yaml
/v1/charges:
  parameters:
    - { name: Idempotency-Key, in: header, schema: { type: string } }
  post:
    tags: [Charges]
    requestBody:
      content:
        application/json:
          schema: { $ref: '#/components/schemas/ChargeCreate' }
```

After normalization:

```
POST /v1/charges  tags=[Charges]
  header  Idempotency-Key  string
  body    amount           integer  required
  body    currency         string   required
  body    customer         string
  body    capture          string   enum=[automatic, manual]
  auth    bearerAuth
```

**In plain words.** The blueprint is written with lots of cross-references ("see page 40"). I follow every reference and rewrite each endpoint as one flat, complete card, so nobody has to flip pages again.

## 7. Step 3: extracting structural claims

**How it works.** One pass over the normalized operations produces the five structural claim types from SPEC §2.2:

| Type | One claim per | Example fact |
| --- | --- | --- |
| `endpoint-exists` | operation | `POST /v1/charges` exists |
| `param-name` | parameter or body field | `customer` is a body field of `POST /v1/charges` |
| `required-field` | required body field | `POST /v1/charges` requires `amount` |
| `enum-value` | field or parameter with an `enum` | `capture` ∈ {`automatic`, `manual`} |
| `auth-scheme` | security scheme in use | the API uses bearer auth |

Rules that keep this predictable:

- Claims are sorted by ID before they leave the adapter.
- Deprecated operations still produce claims but are marked; whether the sampler uses them is a role 4 decision.
- `auth-scheme` is per scheme, not per operation (otherwise one scheme produces thousands of identical claims). It has `operation = None` and its own ID shape (§4).
- The `fact` sentence is generated from a fixed template, never written by hand.

Claim counts per type are reported for every target and version, because the sampler (role 4) needs them for stratified sampling and coverage.

**Example.** From the normalized `POST /v1/charges` above:

```
acme/hard/endpoint-exists/POST-/v1/charges
acme/hard/param-name/POST-/v1/charges/header/Idempotency-Key
acme/hard/param-name/POST-/v1/charges/body/amount
acme/hard/param-name/POST-/v1/charges/body/currency
acme/hard/param-name/POST-/v1/charges/body/customer
acme/hard/param-name/POST-/v1/charges/body/capture
acme/hard/required-field/POST-/v1/charges/body/amount
acme/hard/required-field/POST-/v1/charges/body/currency
acme/hard/enum-value/POST-/v1/charges/body/capture
```

**In plain words.** I turn each endpoint card into a list of short, testable statements, the way a teacher turns a chapter into exam-ready facts.

## 8. Step 4: snippets and slices

**How it works.** Snippets are the text the models see in the `snippet` and `full` modes (SPEC §2.4). Two kinds:

- **Operation snippet**: one per operation, rendered from the normalized card as compact plain text: method, path, summary, description, parameters, body fields, auth. These are what BM25 searches over (role 4).
- **Tag slice**: all operations sharing a tag, used for `full-sliced` when the whole spec doesn't fit a model's context. If an operation has no tag, its first path segment is used (`/v1/charges/...` → `charges`).

Rendering is deterministic: fixed field order, fixed formatting, no timestamps. The same spec always gives byte-identical snippets. `size_bytes` is stored so reports can show slice sizes.

Three more things the modes need from this step:

- **Full document.** The `full` mode gives the model "the whole document if it fits" (SPEC §2.4). Proposal: the full document is all operation snippets joined in sorted order, not the raw spec file. It is far smaller than raw YAML (GitHub's file is many MB) and uses the same rendering as the other modes. To be confirmed with role 4 (open question, §17).
- **Claim → slice.** `full-sliced` uses "the slice containing the claim", so every claim with an operation carries `slice_key`. For `auth-scheme` claims (no operation) it is `None`.
- **Change claims.** A `removed` claim points at something that is not in the current spec, so it has no current snippet. That is intended: the context shows the current API, and the right answer is to not use the removed thing. Its `slice_key` is the slice where the operation lives now, or, for a removed endpoint, the slice it was in before. To be confirmed with roles 1 and 4.

**Example.**

```
POST /v1/charges  (tag: Charges)
Create a charge.
Auth: bearer token
Header: Idempotency-Key (string, optional)
Body:
  amount    integer, required — amount in the smallest currency unit
  currency  string,  required
  customer  string
  capture   string, one of: automatic, manual
```

**In plain words.** Besides the list of facts, I also cut the manual into tidy pages. When a model is allowed to "look things up", these pages are what it gets to read.

## 9. Step 5: change claims with oasdiff

**How it works.** `removed` and `renamed` claims come from comparing consecutive versions with **oasdiff**, not from reading changelog prose (SPEC §2.1, FAQ §2). SPEC keeps changelog prose as supporting evidence only (e.g. showing the release note to a maintainer); that is out of scope for the MVP adapters.

1. For each consecutive pair of versions (`2025-02 → 2025-03`), run `oasdiff changelog old.yaml new.yaml --format json`. oasdiff runs as a pinned Docker image or a pinned binary in our image, so everyone gets the same output.
2. Map the relevant change entries to the claim types: endpoint removed, request parameter removed and request body property removed each become a `removed` claim; added parameters and properties are kept aside for rename pairing. The exact oasdiff check IDs are listed by `oasdiff checks`; the mapping table lives in code and has its own test.
3. **Rename pairing.** oasdiff reports a rename as "removed X" + "added Y". They are paired only when **all** hold: same operation, same location (path / query / header / body), same type, removed and added in the same version step, and it is the **only** possible pair in that operation and location. If two removed and two added fields could pair, the adapter doesn't guess: it emits plain `removed` claims. Being conservative keeps `renamed` claims trustworthy.
4. A change claim records `since_version` (the version where the change happened) and the old name.

**Example.** oasdiff on Acme `2025-02 → 2025-03`, simplified:

```
POST /v1/charges   request property removed   customer_id (string)
POST /v1/charges   request property added     customer    (string)
DELETE /v1/charges/{id}   endpoint removed
```

Result:

```
acme/hard/renamed/POST-/v1/charges/body/customer        old_name=customer_id  since=2025-03
acme/hard/removed/DELETE-/v1/charges/{id}               since=2025-03
```

**In plain words.** I lay last month's blueprint next to this month's and mark every line that disappeared. When a line disappeared and a very similar one appeared in the same spot, I call it a rename, but only when there is no doubt.

## 10. Step 6: the name index for failure causes

**How it works.** When a model's answer fails, role 3 decides *why* (SPEC §2.6). Two causes depend on data from this role: `stale-knowledge` (the request is valid against an **older** version) and `hallucinated` (it uses a name that exists in **no** known version).

This role provides:

1. **Spec files per version**, exported unchanged, so role 3 can start Prism on an older version and re-check the request. Per FAQ §5 I do **not** "tighten" specs; the original constraints are preserved.
2. **A name index**: for every (operation, location, name), the list of versions it appears in.

```json
{
  "POST /v1/charges": {
    "body": {
      "customer_id": ["2023-11", "...", "2025-02"],
      "customer":    ["2025-03", "...", "2025-10"],
      "amount":      ["2023-11", "...", "2025-10"]
    }
  }
}
```

Paths are matched with parameter names ignored (`/v1/charges/{id}` and `/v1/charges/{charge}` are the same path), because specs sometimes rename path placeholders without changing the API.

**Example.** A model sends `customer_id`. The index shows it existed until `2025-02`, so role 3 can label it `stale-knowledge` and say since when. A model sends `client_ref`, which is not in any version, so it is `hallucinated`.

**In plain words.** I keep a register of every name that has ever appeared in the blueprint and when. That's how the project can prove an AI's wrong answer was once right.

## 11. Determinism and testing

**How it works.** The whole project depends on "same input → same output" (SPEC §2.3, §9). For adapters this means: no use of the current time, random numbers or dictionary ordering anywhere in the output; everything sorted by stable keys before writing; canonical JSON (sorted keys, fixed separators) for anything that gets hashed; external tools (oasdiff) pinned to an exact version.

Tests (pytest):

| Test | What it catches |
| --- | --- |
| **Golden files** per adapter step: fixture spec → expected claims, snippets, name index | any accidental change in output |
| Run twice, compare hashes | hidden non-determinism |
| Small hand-written fixture specs with known `allOf`, `oneOf`, `$ref` cycles, form bodies | normalization bugs |
| Two fixture versions with a known rename and removal | oasdiff mapping and pairing rule |
| Ambiguous rename (2 removed, 2 added) | the pairing rule stays conservative |
| Smoke test on the real Stripe, GitHub, Twilio specs (not in every CI run, too slow) | crashes on real-world quirks |

When output changes on purpose, the golden files are regenerated in the same PR, so the reviewer sees exactly what changed. The fixture spec lives in `deploy/fixtures/openapi.yaml` and is shared with the end-to-end test (role 7).

**In plain words.** I save a "correct answer sheet" for the test blueprint. Every time the code changes, the program checks it still produces exactly that sheet, so mistakes can't sneak in unnoticed.

## 12. Technologies

| Need | Choice | Why |
| --- | --- | --- |
| Language | Python 3.12+ | project standard (SPEC §5) |
| Data models | Pydantic v2 | typed, validated, easy JSON; shared with the backend |
| YAML / JSON | PyYAML (`CSafeLoader`), `orjson` | fast enough for multi-MB specs |
| Spec validation | `openapi-spec-validator` | checks OpenAPI 3.0 / 3.1 validity |
| `$ref` resolution | own small resolver | needs cycle handling and to keep source pointers |
| Spec diffs | **oasdiff** (pinned binary / Docker image) | mandatory in SPEC; structured JSON changelog |
| History | `git` CLI via `subprocess` | simple, no extra dependency |
| Testing | pytest, golden files | SPEC §9 |
| Quality | ruff, mypy (strict on `core/`) | SPEC §5 |
| Packaging | uv | SPEC §5 |

Not used here: language models, embeddings, the database. Adapters are pure functions from files to data, which makes them easy to test and reuse in the GitHub Action.

## 13. Code layout and CLI

```
core/src/notinspec/
  model.py                  shared shapes (Claim, Snippet, SpecVersion, …)
  adapters/
    targets.py              target config loading
    history.py              git fetch, version selection, export
    openapi/
      load.py               parse, validate
      refs.py               $ref resolver with cycle guard
      normalize.py          operations, parameters, bodies, security
      claims.py             structural claim extraction
      snippets.py           operation snippets and tag slices
    diff/
      oasdiff.py            running oasdiff, parsing its JSON
      changes.py            removed claims, rename pairing
    name_index.py           names across versions
core/tests/adapters/
  fixtures/                 small specs, two-version fixtures
  golden/                   expected outputs
```

CLI commands (thin wrappers, role 1 owns the overall CLI):

```bash
notinspec adapters fetch  --target stripe              # update repo cache, export versions
notinspec adapters claims --spec openapi.yaml --out claims.jsonl
notinspec adapters diff   --old v1.yaml --new v2.yaml  # change claims between two files
notinspec adapters stats  --target stripe              # claim counts per type and version
```

`stats` is useful early: it shows the real size of each API before anyone runs models on it.

## 14. Handoffs to other roles

| To | What I hand over | What I need back |
| --- | --- | --- |
| 1 Lead / generator | claims in the agreed shape, stable IDs | template needs (e.g. example values from the spec) |
| 3 Runner & verification | spec files per version, name index | which checks need which data |
| 4 Retrieval & evaluation | snippets, slices, claim counts per type | sampling rules, e.g. what to do with deprecated operations |
| 5 Backend & data | `SpecVersion` records with content hashes | how versions and claims are stored |
| 7 DevOps | oasdiff in the image, repo cache volume on the VM | disk space for clones and exported versions |

The roadmap's biggest dependency risk is that roles 1 and 3 build against guessed claim shapes. Agreeing the shapes in week 8 and keeping the fixture outputs up to date avoids that.

## 15. Pitfalls in real specs

| Problem | How it's handled |
| --- | --- |
| Form-encoded bodies (Stripe) | treat `application/x-www-form-urlencoded` as a body location, same as JSON |
| Recursive `$ref`s | cycle guard; stop at the depth limit |
| `anyOf` / `oneOf` everywhere | union of fields; required only if required in all branches |
| Huge files (GitHub) | C YAML loader, parse once per version, cache normalized output by content hash |
| Many files per API (Twilio) | fixed list of files per target in config |
| Path placeholders renamed between versions | match paths with placeholders ignored |
| Spec reformatted, nothing really changed | content hash on normalized output; no new version if equal |
| Invalid spec in an old commit | log it, skip that version, continue with the neighbours |
| Vendor extensions (`x-…`) | ignored in MVP |
| Schemas that allow unknown fields | nothing changes in adapters; role 3 checks the targeted names explicitly (FAQ §5) |

## 16. Plan for weeks 8–12

Aligned with the agreed roadmap (row "Vstupné adaptéry"). The goals are indicative; scope and timing can move with the implementation.

| Week | Roadmap goal | Concrete steps |
| --- | --- | --- |
| 8 · Start of implementation | start processing OpenAPI and getting the data needed for testing | agree `Claim`, `Snippet`, `SpecVersion` shapes with roles 1, 3, 5; loader, validator, `$ref` resolver; fixture spec + first golden file |
| 9 · Development and integration | extract checkable facts and snippets from the spec | normalization of operations, bodies and security; all 5 structural claim types; operation snippets and tag slices; `stats` command |
| 10 · First pass through the system | connect input processing to task generation, start on version history | hand claims to the generator on the fixture spec; repo cache, monthly version selection, export of versions; run on real Stripe, GitHub, Twilio specs |
| 11 · Testing and first results | verify processing on selected inputs, deal with limitations | oasdiff integration, `removed` claims, rename pairing; name index for role 3; fix real-spec quirks found in week 10 |
| 12 · Demo and next steps | stabilize the supported input range, document extension points | golden files for history; smoke tests on real specs; document supported OpenAPI features, known gaps and how to add a new target |

## 17. Open questions

Each item has a proposed answer, to be confirmed with the named role.

- [ ] Do required query/path parameters also produce `required-field` claims, or only body fields? *Proposal: body only, as SPEC §2.2 says.* (lead)
- [ ] Depth limit for nested body fields: 2 levels, or top level only for the MVP? *Proposal: 2 levels.* (lead)
- [ ] Version rule: monthly for all three targets, or tags where available? *Proposal: tags where they exist (see §5, known limit), monthly otherwise.* (lead)
- [ ] Which Twilio spec files are in scope? And merged for Prism, or one Prism per file? (role 3)
- [ ] Deprecated operations: produce claims but let the sampler skip them, or skip them in the adapter? *Proposal: produce them, marked; the sampler decides.* (role 4)
- [ ] `history_from` per target: which first month? *Proposal: about 24 months before the first weekly run, then fixed.* (lead)
- [ ] Full document for the `full` mode: all operation snippets joined, or the raw spec file? *Proposal: snippets joined (§8).* (role 4)
- [ ] Context for `removed` claims in the snippet / full modes (§8). (roles 1, 4)

Noted for the lead, outside this role: FAQ §5 lists a `task-mismatch` failure cause that SPEC §2.6 doesn't have, and the FAQ claim ID example has no location (§4).
