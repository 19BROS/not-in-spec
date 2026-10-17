# NOT-IN-SPEC — Inspiration

Existing projects that do all or part of what [SPEC.md](SPEC.md) describes. For each one: what it does, where it overlaps with us, what we can borrow, and how we differ.

Nothing below combines all of these: claims generated deterministically from OpenAPI, verification against a mock server, failure causes taken from the spec's version history, and weekly re-runs. Each project covers one or two parts.

> Researched October 2026. Numbers quoted by third parties disagree between sources, so they are left out. Check each project's own page before you cite it.

## Overview

| Project | Kind | Overlaps with our… |
|---|---|---|
| [Next.js Evals](#1-nextjs-evals-vercel) | public leaderboard | modes (with / without docs), leaderboard, re-runs |
| [Auth0 Agent Experience Score](#2-auth0-agent-experience-score) | vendor benchmark | modes (with / without context), one product's API |
| [Fern Agent Score](#3-fern-agent-score) | docs grader | docs → AI readiness (the thing we deliberately are *not*) |
| [Browserbase agent-experience skill](#4-browserbase-agent-experience-skill) | agent-based docs test | asking models about your docs, failure analysis |
| [Gorilla / APIBench / BFCL](#5-gorilla--apibench--berkeley-function-calling-leaderboard) | research benchmark + leaderboard | API-call correctness, hallucinated APIs, execution-based checking |
| [GitChameleon](#6-gitchameleon) | research benchmark | version-specific API knowledge, verification by running code |
| [CodeUpdateArena](#7-codeupdatearena) | research benchmark | renamed / changed API knowledge, the "full text" mode |
| [LiveBench](#8-livebench) | public leaderboard | repeated runs, objective scoring without an LLM judge |
| [promptfoo + GitHub Action](#9-promptfoo-and-its-github-action) | eval tool + CI | GitHub Action, PR comment, failing the build |
| [oasdiff](#10-oasdiff) | spec diff tool | change claims (`removed`, `renamed`), CI gating |
| [Context7](#11-context7-upstash) | MCP docs server | the problem (stale model knowledge), the snippet mode |

---

## Benchmarks that measure model knowledge of a product's docs

### 1. Next.js Evals (Vercel)

**Links:** <https://nextjs.org/evals>, code: <https://github.com/vercel/next-evals-oss> (MIT)

**What it does.** A public leaderboard of how well AI coding agents complete real Next.js tasks. Each eval is a small, self-contained Next.js project with a `PROMPT.md` task and a hidden `EVAL.ts` test file (vitest) that the agent never sees. The test result decides pass or fail, not another model. The leaderboard has two columns: a baseline, and "with AGENTS.md", where the agent can read Vercel's bundled Next.js docs. The success rate is pass@4. Results are re-run whenever the evals change, and old results stay visible with their dates.

**Overlap.** This is the closest thing to our project that exists. It answers the same question ("do the docs help models get it right?") with a with/without-docs comparison, like our `none` vs `full` modes. Answers are checked by running code. Results are public.

**What to borrow.**
- **Two columns side by side, baseline vs with docs.** This is the clearest way to show what documentation adds. Our leaderboard could show `none | snippet | full` next to each other for each model.
- **When a new eval is added, models that haven't run it yet count as failed on it,** so every model is scored on the same set. This is how we should treat a claim added to the sample between runs.
- **Superseded results are kept with their date, not overwritten.** This matches our append-only data rule (§6).
- **Hidden tests the model never sees.** Our version of this is the Prism mock server.

**How we differ.** It covers one framework, its tasks are written by hand, and it measures agents (model + harness) rather than bare models. Our tasks are generated from any OpenAPI spec, and we explain *why* an answer failed (e.g. `stale-knowledge`) instead of just recording a fail.

### 2. Auth0 Agent Experience Score

**Link:** <https://auth0.com/docs/get-started/auth0-agent-experience>

**What it does.** Auth0 measures how well Claude Code, GitHub Copilot and Gemini CLI complete Auth0 integration tasks, with and without Auth0's MCP server and Agent Skills, and publishes the result.

**Overlap.** It is an API vendor measuring how well AI assistants use *its own* API, with a context vs no-context comparison. This is the use case our GitHub Action serves for API maintainers.

**What to borrow.** It shows that vendors care about this enough to publish it, which supports our leaderboard. Its "with MCP" condition is a fourth mode we could add later (semester 2 MCP stretch).

**How we differ.** It is a one-off result for one vendor that nobody else can run. Ours is a reusable tool for any OpenAPI spec, re-run on a schedule.

### 3. Fern Agent Score

**Links:** <https://buildwithfern.com/agent-score>, <https://buildwithfern.com/post/agent-score>

**What it does.** A free, open-source benchmark that grades a documentation site from 0 to 100 on how easily AI agents can discover, parse and use it. It works like Lighthouse, but for AI agents. It checks structure and discoverability, and does not check whether models give correct answers.

**Overlap.** Same audience (docs maintainers) and same theme (are my docs AI-ready?).

**What to borrow.** Its checks (does `llms.txt` exist, can the docs be read as Markdown, is the page structure clean) could become a short note next to our medium and soft layers. They would explain *why* the `snippet` mode does badly for a given API. They would not be a score.

**How we differ.** This is exactly what SPEC §1.1 says we are **not** building: a single score for a document. It is a useful contrast for the presentation. Fern says "your docs score 73". We say "3 of 4 models use `customer_id`, which was renamed in 2025-03".

### 4. Browserbase agent-experience skill

**Link:** <https://www.skills.sh/browserbase/skills/agent-experience>

**What it does.** A Claude skill that tests a docs site or SDK. It starts sub-agents with only a one-sentence task and no extra context, records each agent's tool calls, and rates the run on setup friction, speed, efficiency, error recovery and doc quality.

**Overlap.** It asks models to do something with your product and reports where they get stuck. That is close to our list of failing questions.

**What to borrow.** It records the full trace of each attempt. This supports our "store every raw response forever" rule, and its trace view is a good model for our "failed question detail" page in the web UI.

**How we differ.** Its rating is a model's opinion of how the run went, and its tasks are written by hand. Ours are generated deterministically, and a correct answer is decided by Prism.

---

## Research benchmarks on APIs and outdated knowledge

### 5. Gorilla / APIBench / Berkeley Function Calling Leaderboard

**Links:** paper arXiv:2305.15334 (already in [assignment.md](assignment.md)), leaderboard <https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html>, dataset <https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard>

**What it does.** Gorilla showed that LLMs often make up APIs that don't exist, and that giving the model retrieved docs reduces this. APIBench measured it with an AST match against the real API. The follow-up, the Berkeley Function Calling Leaderboard (BFCL), is a public, regularly updated leaderboard for function and tool calling in Python, Java, JavaScript and REST. It checks some answers by AST and some by actually executing the call.

**Overlap.** Our `hallucinated` failure cause, our `snippet` mode (retrieval-aware), and our "structured request, then execute it" verification.

**What to borrow.**
- **AST checks next to executable checks.** BFCL reports both kinds separately and never mixes them. This is the same as our "layers never averaged" rule.
- Its REST category is the closest prior work to our structured-HTTP-request answer format, and is worth reading before we design our JSON answer schema.
- The idea of a "hallucination rate" as its own metric. Ours is the `hallucinated` failure-cause share.

**How we differ.** BFCL gives the model the function signature and tests whether it can call it. We test whether the model *knows* the API, sometimes with no context at all, and we track that across spec versions.

### 6. GitChameleon

**Links:** arXiv:2411.05830 (v1), arXiv:2507.12367 (v2), ACL 2026; code <https://github.com/NizarIslah/GitChameleon>

**What it does.** A set of Python code-completion problems, each tied to a *specific library version* and checked with executable unit tests. It measures whether a model can write code for the version you asked for instead of whichever version it remembers best. The paper reports that even strong models do poorly, and that showing the model its error output only helps a little.

**Overlap.** Version-specific knowledge, checked by running code, not by a judge.

**What to borrow.** Its finding that models fall back to the version they saw most in training is the academic support for our `stale-knowledge` cause. It also suggests we should report *which* old spec version a stale answer matches, not just that it matched an old one.

**How we differ.** It is a fixed, hand-written dataset for Python libraries. We generate tasks from REST APIs and re-run them over time.

### 7. CodeUpdateArena

**Links:** arXiv:2407.06249, code <https://github.com/leo-liuzy/CodeUpdateArena>

**What it does.** 670 program-synthesis tasks. Each task pairs a (synthetic) update to an API function with a problem that needs the updated behaviour. It tests whether a model can use the *new* behaviour, and compares knowledge editing, fine-tuning on docs, and simply adding the update text to the prompt. Adding the update text to the prompt helps a lot. Fine-tuning on the docs alone barely helps.

**Overlap.** Our `renamed` / `removed` claim types, and the `none` vs `full` comparison.

**What to borrow.** Its two metrics: did the model use the *updated* API correctly (UPass), and did that break things that were already fine (SPass). We could adapt this as "newly passing" vs "newly failing" questions between runs. Its result that context beats fine-tuning also supports reporting `full` mode as the main improvement a maintainer controls.

**How we differ.** Its updates are synthetic and fixed. Ours are real changes taken from `oasdiff` on real spec history.

### 8. LiveBench

**Links:** arXiv:2406.19314, ICLR 2025

**What it does.** A general LLM benchmark that adds new questions regularly from recent sources (new competitions, arXiv papers, news) so they can't already be in training data. Every question has an objective ground-truth answer and is scored automatically, without an LLM judge.

**Overlap.** Repeated runs, change over time, and "verified, not judged".

**What to borrow.** Rotating in new questions to limit contamination. In our case, new claims from each new spec version. It also shows a public benchmark can avoid LLM judges completely, which supports using the judge only as a last resort (SPEC §2.5).

**How we differ.** It is general-purpose, not about one product, and does not explain why an answer failed.

---

## Tooling we can reuse or copy

### 9. promptfoo and its GitHub Action

**Links:** <https://promptfoo.dev/docs/integrations/github-action>, <https://github.com/marketplace/actions/test-llm-outputs>

**What it does.** An open-source LLM eval framework with test cases in YAML, deterministic checks plus LLM-graded checks, and response caching. Its GitHub Action runs evals on PRs that touch prompt files and posts a PR comment with a link to a before/after viewer.

**Overlap.** Almost exactly our §7 GitHub Action: run on PR → compare → comment → pass or fail.

**What to borrow.**
- How the PR comment is laid out (summary table + link to details).
- Trigger only on relevant paths (`on.pull_request.paths`).
- Caching responses to keep CI costs down. We already plan this per run.
- **Warning:** sources disagree on whether its action really runs base *and* head, or only the current checkout. Our spec says we run both explicitly. Keep it that way.

**How we differ.** promptfoo tests *your prompts*. We test *your docs*, with the models fixed.

### 10. oasdiff

**Links:** <https://github.com/oasdiff/oasdiff> (formerly `Tufin/oasdiff`)

**What it does.** A CLI and Go library that compares two OpenAPI specs, detects over 100 kinds of breaking change (as errors or warnings), produces changelogs, and has a GitHub Action that fails CI on breaking changes.

**Overlap.** It is already in our stack as the source of `removed` / `renamed` claims (SPEC §2.1).

**What to borrow.** Its list of checks is a ready-made list of future hard-claim types beyond the MVP seven, for example "parameter became required" or "response property removed". Its error/warning split works the same way as our hard/medium layers.

**How we differ.** oasdiff tells the maintainer *what changed*. We tell them *whether AI models noticed*.

### 11. Context7 (Upstash)

**Links:** <https://upstash.com/blog/context7-mcp>, `@upstash/context7-mcp`

**What it does.** An MCP server that gives coding assistants (Cursor, Claude Code, …) current, version-specific library docs when they need them. It has two tools: resolve a library name to an ID, then fetch docs and code examples for that ID up to a token limit.

**Overlap.** It exists to fix the same problem we measure: models answering from outdated training data. Its approach is the same idea as our `snippet` mode.

**What to borrow.**
- It could be a **fourth mode** in an experiment: "context retrieved by Context7" next to our BM25 snippet. That would test whether existing tools actually close the gap we find.
- Its two-step resolve-then-fetch MCP design is a good template for our own MCP server (semester 2 stretch).

**How we differ.** Context7 tries to fix the problem. We measure it, including whether fixes like Context7 work.

---

## Ideas worth taking into the spec

1. **Side-by-side mode columns on the leaderboard** (Next.js Evals): `none | snippet | full` per model, never merged into one number.
2. **Claims added later count as failed for models that haven't run them** (Next.js Evals), so comparisons stay fair.
3. **Report which old version a stale answer matches** (GitChameleon), not just "stale".
4. **More hard-claim types from oasdiff's check list** once the MVP seven are stable.
5. **Experimental fourth mode: an existing context tool (Context7 / MCP)** to see whether the tools people use today close the gap.
6. **Docs-structure checks as context, not as a score** (Fern), to explain poor `snippet` results.
7. **Read BFCL's REST category** before we fix our structured-request JSON schema.

## Sources

- Next.js Evals — <https://nextjs.org/evals>, <https://github.com/vercel/next-evals-oss>
- Auth0 Agent Experience — <https://auth0.com/docs/get-started/auth0-agent-experience>
- Fern Agent Score — <https://buildwithfern.com/agent-score>, <https://buildwithfern.com/post/agent-score>
- Browserbase agent-experience — <https://www.skills.sh/browserbase/skills/agent-experience>
- BFCL — <https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html>, <https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard>
- GitChameleon — <https://huggingface.co/papers/2411.05830>, <https://arxiv.org/abs/2507.12367v1>
- CodeUpdateArena — <https://arxiv.org/pdf/2407.06249>, <https://github.com/leo-liuzy/CodeUpdateArena>
- LiveBench — <https://arxiv.org/abs/2406.19314v1>, <https://iclr.cc/virtual/2025/poster/28134>
- promptfoo — <https://promptfoo.dev/docs/integrations/github-action>, <https://github.com/marketplace/actions/test-llm-outputs>
- oasdiff — <https://pkg.go.dev/github.com/oasdiff/oasdiff@v1.30.0>, <https://github.com/tufin/oasdiff/blob/v1.10.16/BREAKING-CHANGES.md>
- Context7 — <https://upstash.com/blog/context7-mcp>, <https://trevorlasn.com/blog/context7-mcp>, <https://mcpservers.org/remote-mcp-servers/context7>
