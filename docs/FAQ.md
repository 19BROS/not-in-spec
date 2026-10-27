# NOT-IN-SPEC — FAQ

Every technical decision in [SPEC.md](SPEC.md), explained in more detail, with a concrete example and a plain-language paragraph for a non-technical reader.

Each answer has three parts:
- **How it works**: the technical detail.
- **Example**: a concrete case.
- **In plain words**: the same idea for someone who doesn't write code.

> All examples use a made-up API called **Acme Payments**, so nothing here is a claim about a real product.

## Contents

1. [The project](#1-the-project)
2. [Inputs, claims and layers](#2-inputs-claims-and-layers)
3. [Task generation](#3-task-generation)
4. [Asking the models](#4-asking-the-models)
5. [Checking the answers](#5-checking-the-answers)
6. [Results and reports](#6-results-and-reports)
7. [Running over time](#7-running-over-time)
8. [Models, OpenRouter and budget](#8-models-openrouter-and-budget)
9. [Data storage](#9-data-storage)
10. [GitHub Action](#10-github-action)
11. [Web UI](#11-web-ui)
12. [Stack and tooling](#12-stack-and-tooling)
13. [DevOps: Docker, CI, deployment](#13-devops-docker-ci-deployment)
14. [Testing](#14-testing)
15. [Agent formats: AGENTS.md, llms.txt, MCP](#15-agent-formats-agentsmd-llmstxt-mcp)
16. [Project management](#16-project-management)

---

## 1. The project

### What does NOT-IN-SPEC do, in one sentence?

**How it works.** It takes an API's documentation and turns it into a fixed set of test questions. It asks several language models those questions and checks the answers by actually running them against a fake version of the API. It repeats this every week and reports which questions the models get wrong, why, and whether it is getting better or worse.

**Example.** For Acme Payments, the report might say: *"GPT-x answers 41 of 100 questions wrong without context. 18 of those wrong answers use the parameter `customer_id`, which Acme renamed to `customer` in version 2025-03. With the docs provided, only 6 are wrong."*

**In plain words.** Developers now ask AI assistants how to use a product instead of reading its manual. The AI often answers from an outdated memory, and the developer loses time. We built a regular check-up that measures how often AI gets your product wrong, what exactly it gets wrong, and whether the trend is up or down. Think of it as a mystery shopper for your documentation, visiting every week.

### Why isn't it an "upload any document and get an AI-readability score" website?

**How it works.** The assignment rules this out directly:
- *"Instead of a single score, the output is a list of questions the models answer incorrectly, the cause of the failure, and how it evolves over time."*
- Mandatory technologies are OpenAPI, JSON Schema and *"a generated mock server"*. These only make sense for API documentation.
- *"Verified by running code, not by another model's opinion."* A readability score for an arbitrary document could only come from heuristics or an AI's opinion.
- Everything is measured **over time**. A one-off upload has no time dimension.

The only evaluated input is an OpenAPI specification and its version history. Arbitrary document uploads and documentation crawling are outside the agreed scope.

**Example.** A score says *"Your docs: 73/100."* Our output says *"Models think the refund endpoint is `POST /v1/refund`. It is `POST /v1/refunds`. 3 of 4 models get this wrong. It started failing after your March release."* Only the second one tells the maintainer what to fix.

**In plain words.** A single score is like a doctor saying "your health is 7 out of 10". It sounds precise but you can't act on it. We give the diagnosis instead: what exactly is wrong, why, and since when. That's also what the assignment asks for.

### Why is the system one core package with "thin wrappers" around it?

**How it works.** All logic (reading inputs, generating tasks, asking models, checking answers, reports) lives in one Python package, `notinspec`. Four entry points use it without adding logic of their own:

| Wrapper | Who uses it | What it adds |
|---|---|---|
| CLI | developers, the GitHub Action | command-line arguments |
| FastAPI service | the web UI | HTTP endpoints over the database |
| Worker | runs on a schedule | a timer |
| GitHub Action | API maintainers' CI | PR comments, pass/fail |

**Example.** The same function runs in all four places:
```bash
notinspec run --spec openapi.yaml --models free-panel --modes none,snippet,full
```
The worker calls the same code every Monday. The GitHub Action calls it on every PR.

**In plain words.** We build one engine and put it into several cars. Fixing the engine fixes all of them. Building four separate engines would mean four times the bugs and four times the work.

---

## 2. Inputs, claims and layers

### What is a "claim"?

**How it works.** A claim is one checkable fact taken from the documentation, together with **how to verify it**. Every input is first converted into:
- **snippets**: short pieces of the original text (used later as context for the models), and
- **claims**: facts with a verification method attached.

**Example.**
```yaml
id: acme/hard/required-field/POST-/v1/charges/amount
layer: hard
fact: "POST /v1/charges requires the body field `amount` (integer)"
verify: execute-against-mock
source: openapi.yaml#/paths/~1v1~1charges/post
```

**In plain words.** We break the manual into individual statements we can test, like a teacher turning a textbook chapter into exam questions. Each statement also says how it will be marked.

### What is the hard layer, and why is it the only verification layer?

**How it works.** All evaluated claims come from an OpenAPI specification and its version history. The model returns a structured HTTP request. Code checks its format, conformance to the current spec and satisfaction of the task; Prism supplies the mock server. No model grades another model's answer.

**Example.** A task requests 10 charges. The request must use the correct operation and the current parameter name and location, with the value 10. A request that the mock accepts but that requests 20 charges fails the task.

**In plain words.** We test concrete API requests against the official blueprint and the question asked. The three context modes remain, but all use this same checking method.

### What does the OpenAPI adapter do?

**How it works.** It reads an OpenAPI 3.x file (the machine-readable description of every endpoint, parameter and field) and walks it to produce hard claims: every operation, parameter, required field, enum and auth scheme. It also splits the spec into snippets by operation and tag, which are used for the "snippet" and "full-sliced" modes.

**Example.** This fragment of the spec:
```yaml
paths:
  /v1/charges:
    post:
      tags: [Charges]
      requestBody:
        content:
          application/json:
            schema:
              required: [amount, currency]
              properties:
                amount:   { type: integer }
                currency: { type: string }
                capture:  { type: string, enum: [automatic, manual] }
```
produces claims like:
- `endpoint-exists`: `POST /v1/charges`
- `required-field`: `amount`, `currency`
- `enum-value`: `capture` ∈ {`automatic`, `manual`}

**In plain words.** The OpenAPI file is the official, machine-readable blueprint of an API. The adapter reads that blueprint and lists every fact in it that an AI could get wrong.

### Where do "removed" and "renamed" claims come from? What is oasdiff?

**How it works.** Changelogs are written as prose and every company writes them differently, so parsing them reliably is hard. Instead, we take **old versions of the OpenAPI spec from the API's public git repository** and compare consecutive versions with **oasdiff**, a tool that lists differences between two OpenAPI files.
- A **removal** comes straight from oasdiff.
- A **rename** appears in oasdiff as "removed X" plus "added Y". We pair them with a fixed rule: same operation, same location (query/body/…), same type, changed in the same version. That pair becomes a `renamed` claim.
- Changelog text is only used as supporting evidence (e.g. to show the maintainer the release note).

**Example.** Simplified diff between Acme v2024-11 and v2025-03:
```
POST /v1/charges  request body  removed property  customer_id (string)
POST /v1/charges  request body  added property    customer    (string)
DELETE /v1/charges/{id}         endpoint removed
```
Resulting claims:
- `renamed`: `customer_id` → `customer` in `POST /v1/charges`
- `removed`: `DELETE /v1/charges/{id}` no longer exists

**In plain words.** Instead of reading the product's release notes, which can be vague, we compare last year's blueprint with this year's, line by line. That shows exactly what was removed or renamed. These are the facts an AI trained on old data is most likely to get wrong.

---

## 3. Task generation

### Do we write the ~100 questions by hand?

**How it works.** No. We write **one template per claim type**, not one per question. For the MVP that's about 7 templates (`endpoint-exists`, `param-name`, `required-field`, `enum-value`, `auth-scheme`, `removed`, `renamed`). The code does everything else:
1. The **adapter** reads the spec and lists every claim in it. For a large API that's thousands (see §2).
2. The **sampler** picks ~100 of them with a fixed seed, so the same 100 are picked every run. "100" is just the sample size we set, not a number of questions anyone writes.
3. The **generator** fills each picked claim into its type's template, and that's the question.

So the work is writing ~7 templates plus the code for the adapter, sampler and generator. It is not writing 100 questions.

**Example.** One template for `required-field`:
```
Using the {api} API, call {method} {path}.
Respond only with the HTTP request as JSON matching the given schema.
```
Filled from the claim `POST /v1/charges requires amount`, it becomes:
```
Using the Acme Payments API, call POST /v1/charges.
Respond only with the HTTP request as JSON matching the given schema.
```
The same template covers all 640 `required-field` claims in Acme.

**In plain words.** We don't write the exam questions one by one. We write a few question "forms" with blanks, and the program fills in the blanks from the manual. Seven forms are enough to produce thousands of questions, and we pick the same 100 of them each week.

### How are test tasks generated, and why "deterministically"?

**How it works.** Every claim type has a **fixed question template**. The generator fills it in from the claim. No language model writes or rewrites questions. The process:

1. Adapters produce the full list of claims.
2. Claims are sorted by a stable ID.
3. A sample is drawn with a fixed random seed (see the next question).
4. Each sampled claim is filled into its type's template, together with machine-checkable expected conditions for the requested operation, names, locations and values.
5. Each task is combined with each mode (none / snippet / full).
6. The whole task set is hashed. Same input + same generator version = same hash. A test enforces this.

Templates have a version number. Changing a template changes the generator version, which is recorded with every result, so results from different template versions are never compared by mistake.

**Example.** Claim `renamed: customer_id → customer in POST /v1/charges` with the template for `renamed`:
```
Using the Acme Payments API, create a charge of 10 EUR for customer "cus_123".
Respond only with the HTTP request as JSON matching the given schema.
```
Expected: the model uses `customer`. If it uses `customer_id`, it fails, and the cause is `stale-knowledge`.

The expected conditions are derived from the spec and task parameters, so the verifier checks both API validity and what the task actually asks for.

**In plain words.** The exam questions are written by a fixed recipe, not by an AI. So the same manual always produces exactly the same exam. That's what makes week-to-week comparison fair. If the questions changed each time, we couldn't tell whether the AI got worse or the exam got harder. It also prevents a circular setup where one AI writes the questions another AI is graded on.

### Why sample only ~100 claims per API? What is stratified sampling?

**How it works.** A large API can produce thousands of claims. With 3 modes × 4 models, every claim costs 12 model requests, and free-tier limits are low (§8). So each run uses a **fixed sample of about 100 claims**:
- **Stratified**: the sample is split evenly across claim types (e.g. ~14 per type for 7 hard types), so the rare but important `removed`/`renamed` claims aren't drowned out by thousands of `param-name` claims.
- **Fixed seed**: the same claims are picked every run, so runs are directly comparable.
- **Coverage** is reported: e.g. *"100 of 3,412 claims sampled (2.9%)"*.

When the spec changes, new claims can enter the pool. The seed keeps the choice stable for claims that didn't change.

**Example.**
```
Acme claims: 3,412 total
  endpoint-exists 210 → 14 sampled
  param-name     1,980 → 14 sampled
  required-field   640 → 14 sampled
  enum-value       380 → 14 sampled
  auth-scheme        4 → 4 sampled (all)
  removed           96 → 14 sampled
  renamed           22 → 14 sampled
```
(The leftover places go to the other types in a fixed order.)

**In plain words.** We can't afford to ask every possible question every week. Like an opinion poll, we ask a carefully chosen, representative group of questions. We always ask the same group, so the results stay comparable from week to week.

---

## 4. Asking the models

### Does the model keep trying until it gets the answer right?

**How it works.** No. Each task × model × mode has one answer per run. Incorrect answers, refusals and malformed output are recorded without feedback or a repair attempt. The three modes are independent experiments, not successive attempts to fix an answer. Rate-limit or transport retries apply only when no answer was obtained; infrastructure errors are tracked separately. Resuming a run reuses completed answers.

**Example.** Model-A uses `customer_id` in the `none` condition and fails. That failure stays recorded. A separate `snippet` condition starts with its own prompt and no earlier answer. Next week's run asks again to measure change over time.

**In plain words.** We record the first answer under each set of conditions. A weekly check measures whether the model changed; it does not coach the model until it passes.

### What are the three modes?

**How it works.** Every task is evaluated once in each of three independent conditions, with different context. No previous answer or verification feedback is carried between conditions:

| Mode | Context in the prompt | What it measures |
|---|---|---|
| `none` | nothing | what the model "remembers" from training |
| `snippet` | the top few snippets found by search (BM25) | whether a typical AI coding tool with search would get it right |
| `full` / `full-sliced` | the whole document, or the relevant section if it's too big | whether the docs themselves are clear enough |

Comparing the modes shows **where** the problem is:
- wrong in `none`, right in `snippet` → the model is outdated, but the docs are fine
- wrong even in `full` → inspect the model response, supplied context and task; this alone does not prove the docs are wrong

**Example.**
```
Question: rename customer_id → customer
  none     model-A uses customer_id   ✗ stale-knowledge
  snippet  model-A uses customer      ✓
  full     model-A uses customer      ✓
```
Conclusion: the docs are fine. The model just needs them provided.

**In plain words.** We test the AI three ways: from memory, with a quick search, and with the full manual open. If it fails from memory but passes with the manual, the AI is out of date. If it fails even with the manual open, we inspect the failure; the model, context handling or documentation may be responsible.

### How does the "snippet" mode find snippets? What is BM25, and what are embeddings/pgvector?

**How it works.**
- **BM25** is a classic keyword search ranking (the kind behind most search engines before AI). It scores snippets by how often the question's words appear in them, weighted by how rare those words are. It's fast, needs no AI model, and gives the same result every time. We use the `rank_bm25` Python library.
- **Embeddings** turn text into lists of numbers so that texts with similar *meaning* end up close together, even with different words. **pgvector** is a PostgreSQL extension that stores these and searches them. This is a semester-2 experiment, reported separately from BM25.

**Example.** Question: *"How do I create a charge for a customer?"* BM25 ranks the `POST /v1/charges` snippet first because of the rare word "charge". An embedding search might also find a page titled "Billing a client", which BM25 would miss because none of the words match.

**In plain words.** In this mode we simulate an AI assistant that searches the docs before answering. We start with a simple, predictable search method (like the search box on a website) and later try a smarter "search by meaning" to see whether it helps.

### What is "full-sliced"?

**How it works.** A large API spec can be several megabytes, much more than a model can read at once (its "context window"). If the whole document fits, we send it all (`full`). If not, we send the **section of the spec containing the claim**, cut by a fixed rule: the OpenAPI tag or resource the operation belongs to (`full-sliced`). The slice size is recorded for every task so results stay interpretable.

**Example.** The claim is about `POST /v1/charges`, which is tagged `Charges`. The full Acme spec is 4 MB, so the model gets only the `Charges` section (~60 KB), and the task is labelled `full-sliced (60 KB)`.

**In plain words.** Some manuals are too thick for the AI to read in one go. In that case we give it the whole relevant chapter instead of the whole book, and we note that we did.

### Why must the model answer in a structured JSON format?

**How it works.** For hard claims, the model must reply with a JSON object describing the HTTP request it would send, matching a fixed schema (method, path, query, headers, body). Many models can be forced to follow a schema ("structured output"). This means:
- no AI is needed to understand the answer
- the answer can be sent straight to the mock server
- a reply that doesn't match the schema is itself a result (`malformed-output`)

**Example.** Expected answer format:
```json
{
  "method": "POST",
  "path": "/v1/charges",
  "query": {},
  "headers": { "Authorization": "Bearer <API_KEY>" },
  "body": { "amount": 1000, "currency": "eur", "customer": "cus_123" }
}
```

**In plain words.** Instead of letting the AI answer in a paragraph that someone would have to read and interpret, we make it fill in a strict form. A form can be checked automatically and objectively.

---

## 5. Checking the answers

### What is Prism and how does the mock server check answers?

**How it works.** Prism reads the OpenAPI spec and serves a mock API. We validate the model's output format, send its request to the mock, and combine the validation result with deterministic checks against the source spec and the task's expected conditions. A pass requires all checks to succeed. A successful HTTP status by itself does not establish correctness.

**Example.** The task asks for charges belonging to customer `cus_123`. The current body field is `customer`, but the model sends `customer_id`. Even if the schema permits additional properties and the mock accepts the request, our task-condition check fails it because the requested customer was not supplied under the correct field.

**In plain words.** We try the request against a fake API and also check that it does what the question asked. Another AI does not decide the result.

### Do we have to build the mock server ourselves?

**How it works.** No. Prism is an existing tool, so we write no mock code. We give it the spec file, and it serves a fake API that matches that spec. In Docker Compose it is a single service. Our code sends the model's JSON request, reads validation results, and checks the task conditions and targeted spec elements. If the spec changes, we restart Prism with the new file. Nothing needs to be rewritten.

The only spec we write by hand is a **small fixture spec** for the automated tests (§14), so the tests don't depend on a real API.

**Example.** The whole mock server in `docker-compose.yml`:
```yaml
prism:
  image: stoplight/prism:5
  command: mock -h 0.0.0.0 /specs/acme.yaml
  volumes:
    - ./specs:/specs
```
The model answers `POST /v1/charges` with the requested values → mock validation and task checks both succeed → **pass**.
The model leaves out `amount` → Prism replies `422` → **fail**.

**Important.** Real specs may permit additional properties, and a mock may ignore unknown query parameters. The verifier explicitly checks the targeted parameter/field names, locations and requested values. We preserve the original spec rather than silently changing its constraints.

**In plain words.** We don't build the replica of the front door ourselves. A ready-made tool builds it straight from the blueprint. When the blueprint changes, we just hand the tool the new one.

### How do you know *why* an answer failed? What is "stale-knowledge"?

**How it works.** When a hard answer fails against the current spec, we also check it against **older versions of the spec** (which we already have from the oasdiff history). Then a fixed set of rules decides the cause:

| Cause | Rule |
|---|---|
| `stale-knowledge` | the request is valid against an older spec version |
| `hallucinated` | uses a name absent from all inspected spec versions |
| `wrong-location` | right name, wrong place (query instead of body, etc.) |
| `missing-required` | a required field is missing |
| `invalid-value` | wrong type or enum value |
| `wrong-auth` | wrong authentication |
| `task-mismatch` | valid API request, but wrong requested operation or values |
| `malformed-output` | the answer doesn't match the JSON schema |
| `refusal` | the model refused or said "I don't know" |

**Example.** The `customer_id` request above fails against v2025-03 but **passes against v2024-11**. Cause: `stale-knowledge` (valid until 2025-03). If the model had used `client_ref`, which never existed, the cause would be `hallucinated`.

**In plain words.** We don't just mark answers wrong, we find out why. The most interesting case: the AI's answer *used to be* correct. It learned from an old version of the manual and nobody told it things changed. We can prove this because we keep every old version of the blueprint and try the answer against them.

---

## 6. Results and reports

### What does the report show, and why no single score?

**How it works.** The main table is **accuracy per API × mode × model**. Next to it:
- **coverage**: sampled claims / total claims in the OpenAPI-derived pool
- **failure-cause distribution**: e.g. 60% stale-knowledge, 25% hallucinated
- **delta vs previous run**: change in percentage points
- **newly failing / newly passing questions**: the most actionable part

**Example.** If 73 of 100 evaluated tasks pass, accuracy for that API, model and mode is 73%. This is a summary statistic, not a primary 73/100 points grade. The sample size is configurable (about 100 is the budget cap), and the report still leads with failing questions, causes and history. Infrastructure errors and unfinished tasks are shown separately.
```
Acme / hard / none
             accuracy   Δ vs last week   top cause
model-A      58% ±10    −7 pp ▼          stale-knowledge (12)
model-B      71% ±9     +1 pp            hallucinated (5)

Newly failing (model-A):
  - renamed customer_id → customer   (stale-knowledge)
  - removed DELETE /v1/charges/{id}  (stale-knowledge)
```

**In plain words.** We don't give a grade. We give a to-do list: these questions are failing, this is why, and these started failing this week. A grade tells you how you're doing. A to-do list tells you what to fix.

### What are the "±" numbers (bootstrap confidence intervals)?

**How it works.** With ~100 questions, one or two lucky or unlucky answers move the percentage noticeably. A **95% confidence interval** gives the range the true accuracy probably lies in. **Bootstrapping** computes it by re-sampling the results thousands of times. It needs no statistical assumptions and is easy to implement.

**Example.** 62 of 100 correct → **62%, interval ≈ 52–72%**. If last week was 66% (56–75%), the intervals overlap a lot, so "−4 pp" is probably noise, not a real drop. The UI shows this so nobody panics over random variation.

**In plain words.** If you flip a coin 10 times and get 6 heads, that doesn't prove the coin is unfair. Our "±" tells you how much of a change is real and how much is just chance.

---

## 7. Running over time

### How do scheduled runs, diffs and alerts work?

**How it works.**
- The **worker** container runs each target API **weekly**, and also when it notices the input changed (e.g. a new spec commit).
- Every run is compared ("diffed") with the previous run of the same target, model and mode on comparable task IDs. Added/removed tasks and input or generator changes are shown separately.
- If accuracy for any API × mode × model drops by more than a threshold (default **5 percentage points**), a message is posted to **Slack**.
- Runs are **resumable**. If the daily API limit is reached halfway, the run pauses and continues the next day from where it stopped.

**Example.** Slack message:
```
⚠ notinspec: Acme / hard / none / model-A dropped 66% → 58% (−8 pp)
  New failures: 5 (4× stale-knowledge, 1× hallucinated)
  Likely trigger: Acme spec v2025-03 (customer_id renamed)
  → https://notinspec.example/acme/runs/2025-03-17
```

**In plain words.** The system checks every week by itself and only bothers the team when something actually gets worse. It's like a smoke alarm: silent most of the time, loud when it matters.

### What is APScheduler and why not Celery/Redis?

**How it works.** **APScheduler** is a Python library that runs functions on a schedule (like a built-in alarm clock). It runs in its own `worker` container and stores job state in the same PostgreSQL database. **Celery + Redis** is the heavier standard for distributed task queues. It would add a message broker, more containers and more failure points, which we don't need for a few runs per week.

**Example.**
```python
scheduler.add_job(run_target, "cron", day_of_week="mon", hour=3, args=["acme"])
```

**In plain words.** We need a reliable alarm clock, not a full logistics company. We picked the simplest tool that does the job, so there's less to break and less to maintain.

---

## 8. Models, OpenRouter and budget

### What is OpenRouter and why use it?

**How it works.** **OpenRouter** is a single API that forwards requests to many model providers (OpenAI, Anthropic, Google, Meta, Mistral, …). It uses the same request format as OpenAI's API. One account and one key give access to many models, including **free ones** (model IDs ending in `:free`).

**Example.**
```python
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
client.chat.completions.create(model="<provider>/<model>:free", temperature=0, messages=...)
```

**In plain words.** Instead of opening accounts with ten AI companies, we use one service that connects to all of them, much like a travel site that sells tickets from many airlines.

### Why do the free-tier limits matter so much? Why do we need $10?

**How it works.** OpenRouter's free models allow **20 requests/minute** and **50 requests/day per account**, raised to **1,000/day once at least $10 of credits has been purchased** ([OpenRouter limits](https://openrouter.ai/docs/limits)). Limits apply per account, not per key.

One run of one API = 100 claims × 3 modes × 4 models = **1,200 requests**.

| Budget | Requests/day | 3 APIs weekly need ~3,600 | Result |
|---|---|---|---|
| $0 | 50 | ~72 days | impossible; ~1 API run per month |
| **$10 once** | 1,000 | ~4 days | **weekly works** |

Verification uses code and Prism, so no additional model calls are needed to grade answers. Transport retries and interrupted calls can still affect actual quota usage.

**In plain words.** The free plan lets us ask about 50 questions a day. One weekly check-up needs about 3,600. A one-time $10 purchase raises the daily allowance 20×, which is the difference between a working project and one that can't do its main job. It's the cheapest item in the whole project and the most important.

### Why temperature 0, and what about models disappearing?

**How it works.**
- **Temperature** controls randomness. At 0 the model picks its most likely answer, which makes runs as repeatable as possible. Providers don't guarantee identical output even at 0, which is one more reason we store every raw response.
- Every request records the **exact model ID and all parameters**, so results are never mixed between model versions.
- Free models get added and removed without warning. A missing model is shown on the leaderboard as **"unavailable since <date>"**, not treated as a crash.

**Example.** `model-C:free` disappears in week 12. Its history stays visible with a gap marker. The panel continues with the other 3 models, and a replacement starts a new history line.

**In plain words.** We keep the AI's "creativity" turned off so it answers the same way every time, and we note exactly which version answered. If a free model is withdrawn, we show that honestly instead of letting the system break.

### Why is the response cache limited to one run?

**How it works.** Responses are cached by **(run ID, model, prompt hash)**. If a run is interrupted and resumed, already-answered questions aren't asked again, which saves quota. The cache **never crosses runs**. If next week reused last week's answers, we'd never notice a model changing, and measuring change over time is the whole point.

**In plain words.** If we get interrupted halfway through an exam, we don't make the student redo the questions they already answered. But next week is a new exam, and they answer everything again.

---

## 9. Data storage

### Why PostgreSQL, and why "append-only" raw responses?

**How it works.**
- **PostgreSQL** is a reliable, free relational database. We access it through **SQLAlchemy 2** (Python database toolkit) and manage schema changes with **Alembic** (versioned migrations).
- Raw model responses are stored in a **JSONB** column (JSON stored efficiently and searchable) and are **never updated or deleted**. Last month's model answers can't be recreated later, because the model may have changed or disappeared. This dataset is one of the project's main outputs.
- Every result row records its **provenance**: input snapshot hash, spec version, generator version, task ID, mode, model ID and parameters, raw response, verdict, failure cause, timestamps.
- Regular `pg_dump` backups are copied off the VM.

**Example.** One stored result:
```json
{
  "run_id": "2025-03-17-acme",
  "task_id": "acme/hard/renamed/POST-/v1/charges/customer",
  "mode": "none",
  "model": "<provider>/<model>:free",
  "params": { "temperature": 0 },
  "spec_version": "2025-03",
  "generator_version": "1.4.0",
  "raw_response": "{ \"method\": \"POST\", ... \"customer_id\": \"cus_123\" }",
  "verdict": "fail",
  "cause": "stale-knowledge",
  "valid_in_version": "2024-11"
}
```

**In plain words.** We keep every answer every AI ever gave us, untouched, with a label saying exactly when and under what conditions. It's like a scientific lab notebook: you never erase entries, because you can't go back in time to redo the experiment.

---

## 10. GitHub Action

### What does the GitHub Action do?

**How it works.** **GitHub Actions** is GitHub's built-in automation (CI). Our **reusable action** lets any API maintainer add NOT-IN-SPEC to their own repository:
1. It triggers on a pull request that changes the OpenAPI spec.
2. Inside the GitHub runner, it starts Prism and runs our CLI twice: on the **base branch** and on the **PR branch**.
3. It posts a PR comment with the questions that newly fail.
4. It **fails the build** if hard-layer accuracy drops by more than a configurable threshold.

The user provides their own OpenRouter key as a repository secret. Our hosted service isn't needed.

**Example.** Workflow in the maintainer's repo:
```yaml
on:
  pull_request:
    paths: ["openapi.yaml"]
jobs:
  notinspec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: <our-org>/notinspec-action@v1
        with:
          spec: openapi.yaml
          max-drop-pp: 5
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
```
PR comment:
```
notinspec: hard-layer accuracy 74% → 61% (−13 pp) ✗
Newly failing:
  - POST /v1/charges  field `customer`: models still use `customer_id`
    → consider documenting the rename in the field description
```

**In plain words.** It's an automatic check that runs whenever someone edits the documentation. If the edit makes AI assistants understand the product worse, it blocks the change and explains why, much like a spellchecker that refuses to save a document full of mistakes.

### Why do we dogfood it on a demo API instead of Stripe-size APIs?

**How it works.** Each PR check runs the suite twice. On a large API that would quickly exceed free limits. A small **demo API repo** that we control lets us create realistic PRs (rename a field, remove an endpoint) and show the Action catching them, within budget.

**In plain words.** We test our smoke alarm in our own kitchen, where we can safely light the match, instead of in someone else's building.

---

## 11. Web UI

### What does the web interface show, and why is it read-only?

**How it works.** A **React + Vite + TypeScript** single-page app, served as static files by **nginx**, reads data from our FastAPI service. Charts use **ECharts or Recharts**. Pages:
- **Leaderboard**: target APIs side by side, per API/mode/model
- **API detail**: failing questions with causes, filterable
- **History**: accuracy over time, with markers for spec releases and model changes
- **Question detail**: every raw answer for one question across runs

There are no user accounts. Everything public is read-only. Admin actions (add a target, trigger a run) go through the CLI or a token-protected API endpoint.

**Example.** The history chart for Acme shows model-A's hard/none accuracy at ~68% for months, dropping to 58% the week the 2025-03 spec was released. Clicking the drop lists the renamed `customer_id` questions.

**In plain words.** It's a public scoreboard and a detailed report in one website. Anyone can look, nobody needs to log in, and nobody can change the data from the website. That keeps it simple and safe.

---

## 12. Stack and tooling

### Why Python 3.12 and FastAPI?

**How it works.** Python 3.12+ is mandatory. **FastAPI** is the recommended Python web framework. It's fast, uses type hints, and **generates an OpenAPI spec of our own API automatically**. We validate that generated spec in CI, which also covers the mandatory "OpenAPI + validation" requirement for our own service.

**In plain words.** Python is required by the assignment and is the standard language for AI work. FastAPI automatically writes the blueprint of our own system, so we follow the same practice we're measuring in others.

### What are uv, ruff, mypy, pytest and pre-commit?

**How it works.**

| Tool | What it does |
|---|---|
| **uv** | installs Python and dependencies, very fast, with a lockfile so everyone has identical versions |
| **ruff** | lints and formats code (finds mistakes and style problems in milliseconds) |
| **mypy** | checks type hints, catching a class of bugs before code runs. Used on `core/` |
| **pytest** | runs tests |
| **pre-commit** | runs ruff (and similar checks) automatically before every commit |

**Example.**
```bash
uv sync            # install exactly the locked versions
uv run pytest      # run tests
uv run ruff check  # lint
```

**In plain words.** These are the workshop's standard tools: one installs the materials, one checks the work for mistakes, one runs the quality tests. Seven people working in one codebase need the same tools, or nothing fits together.

### Why one repository (monorepo)?

**How it works.** All parts live in one git repository:
```
core/    package + CLI          worker/  scheduler
api/     FastAPI service        web/     React SPA
action/  GitHub Action          deploy/  docker-compose, nginx
docs/    SPEC, FAQ, INSPIRATION, assignment
```
A change that touches several parts (e.g. a new field shown in the UI) is one PR, reviewed and tested together.

**In plain words.** One shared folder for the whole team instead of seven separate ones, so a change and everything it affects travel together.

---

## 13. DevOps: Docker, CI, deployment

### What do Docker and Docker Compose do here?

**How it works.** **Docker** packages each service with everything it needs into an "image" that runs identically anywhere. **Docker Compose** starts several containers together from one file. Ours: `postgres`, `api`, `worker`, `prism`, `web` (nginx).

**Example.**
```bash
docker compose up -d   # whole system running locally or on the VM
```

**In plain words.** Each part of the system is shipped in a sealed box that works the same on a laptop and on the server. Compose is the instruction sheet that says which boxes to start and how to connect them. "It works on my machine" stops being a problem.

### What does the CI pipeline do? What is GHCR?

**How it works.** On every push and PR, GitHub Actions:
1. lints (ruff, mypy, oxlint)
2. runs unit tests
3. starts the system with Compose and runs integration tests
4. builds Docker images and pushes them to **GHCR** (GitHub Container Registry, GitHub's free storage for Docker images)

**In plain words.** Every change is automatically checked and packaged by a robot before it can reach the live system. Mistakes are caught within minutes, not after release.

### How do we deploy to a faculty VM that's only reachable over VPN?

**How it works.** GitHub's servers can't reach a VM behind the faculty VPN. A **self-hosted GitHub runner** solves this: a small agent installed on the VM that **connects out** to GitHub and asks for jobs, so no inbound access is needed. On a push to `main`, the deploy job runs on the VM: `docker compose pull && docker compose up -d`.

**Security:** our repo is public. A self-hosted runner on a public repo could let anyone's pull request run code on the faculty VM. So:
- the runner has a dedicated label and is used **only** by the deploy job, only on pushes to `main`
- the deploy job uses a protected `production` environment
- workflows from fork PRs require maintainer approval, and fork PRs never run on the VM

**Example.**
```yaml
deploy:
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  runs-on: [self-hosted, notinspec-vm]
  environment: production
  steps:
    - run: docker compose -f deploy/docker-compose.yml pull
    - run: docker compose -f deploy/docker-compose.yml up -d
```

**In plain words.** The faculty server is behind a locked gate we can't open from outside. So we place a trusted courier inside, who regularly asks GitHub "anything new to install?" and does it. Because our code is public, the courier only accepts orders from the team's official main branch, never from strangers.

---

## 14. Testing

### How do we test something whose output depends on AI models?

**How it works.**
- **Determinism tests**: the same input must always give the same task-set hash. **Golden files** (saved expected outputs) per adapter catch accidental changes.
- **Fake LLM provider**: tests replay **recorded** model responses instead of calling OpenRouter. CI never uses the real API, so tests are free, fast and repeatable.
- **Integration test**: Compose up, Prism with a small fixture spec, then a full run end-to-end using the fake provider.
- **Schemathesis**: generates many random but valid requests from our own API's OpenAPI spec and checks the server doesn't crash or violate its spec.
- **Playwright**: opens the web UI in a real browser and clicks through the main pages.
- **Coverage gate** on `core/` only, where the critical logic lives.

**Example.** A determinism test:
```python
def test_generator_is_deterministic():
    a = generate(load_spec("fixtures/acme.yaml"), seed=42)
    b = generate(load_spec("fixtures/acme.yaml"), seed=42)
    assert task_set_hash(a) == task_set_hash(b)
```

**In plain words.** We can't test with real AIs every time, since that's slow, costs quota, and they answer differently. So we record real answers once and replay them in tests, like rehearsing with a recording of the orchestra instead of booking the orchestra every time.

---

## 15. Agent formats: AGENTS.md, llms.txt, MCP

### What are AGENTS.md, llms.txt and MCP, and what do we do with each?

**How it works.**

| Format | What it is | Our use |
|---|---|---|
| **AGENTS.md** | a file in a repo telling AI coding tools (Claude Code, Codex, …) how the project works: commands, conventions | in our repo, so the team's own AI tools work better |
| **llms.txt** | a file a website publishes for AI tools: a summary plus links to the important pages | publish **our own** as project documentation; it is not an evaluated input |
| **MCP** (Model Context Protocol) | a standard way for AI assistants to call external tools and data | stretch goal: an MCP server that answers "which questions do models get wrong about API X?" |

**Example.** With the MCP server, a developer asks Claude Code: *"Before I integrate Acme, what do models usually get wrong about it?"* The assistant calls our MCP tool and gets: *"customer_id was renamed to customer in 2025-03; models still use the old name."*

**In plain words.** These are the new standard ways for products to talk to AI assistants. We use them for our own project, and later we may let AI assistants ask our system directly for warnings about common API mistakes.

---

## 16. Project management

### Why do weekly runs need to start by mid-semester 1?

**How it works.** The long-term dataset only starts when the first run happens. Past model answers can't be collected retroactively. Every week of delay is a permanent gap in the main deliverable. So semester 1 aims for the hard layer working end-to-end on Stripe, GitHub and Twilio, running weekly, before polishing the reports and adding optional features.

**In plain words.** You can't go back and record last month's weather. The sooner the recorder is switched on, the more valuable the history becomes. Extra features can come later. Lost weeks can't be recovered.

### What is in semester 1 vs semester 2?

**How it works.**
- **Semester 1 (MVP):** OpenAPI + oasdiff adapter, hard claims, generator, 3 modes, runner, Prism verification, failure causes, CLI, database, worker with Slack alerts, basic web UI, CI/CD, weekly runs.
- **Semester 2:** public GitHub Action + demo repo, leaderboard polish, embedding retrieval experiment, MCP server (stretch), evaluation write-up. Verification remains hard layer only.

**In plain words.** First we build the part that can be measured most precisely and start collecting data. Then we improve reporting and retrieval, build the tool for API maintainers, and write up what we learned.

### How are the 7 roles split?

**How it works.**

| # | Role | Owns |
|---|---|---|
| 1 | Lead / architecture | core package, task generator, SPEC.md |
| 2 | Input adapters | OpenAPI, oasdiff history |
| 3 | Runner & verification | OpenRouter client, rate limiting, Prism, task-condition checks, failure causes |
| 4 | ML / evaluation | retrieval, sampling, coverage, statistics, stale-knowledge analysis |
| 5 | Backend & data | FastAPI, Postgres schema, migrations, worker |
| 6 | Frontend & viz | web UI, leaderboard, charts |
| 7 | DevOps | CI, Compose, GHCR, self-hosted runner, GitHub Action, monitoring |

The core package is the shared contract. Each role owns one stage of the pipeline, so people can work in parallel without stepping on each other.

**In plain words.** Like an assembly line: each person owns one station, and the core package is the conveyor belt that connects them.

### Why a public repo and MIT license? Can we publish the model answers?

**How it works.** The assignment's outputs include a **public** leaderboard and dataset, so the code is open too. **MIT** is the simplest permissive license. Open item: some model providers' terms may limit publishing their outputs. Check each free model's terms before publishing the raw dataset (SPEC §12).

**In plain words.** We're building a public good, so everything is open. Before we publish the AIs' answers, we'll check that each AI provider allows it.
