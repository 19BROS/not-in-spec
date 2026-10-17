# Team Project 2026/2027

**Project number: 8**

| | |
|---|---|
| **Topic** | How well do language models understand your documentation? |
| **Acronym** | NOT-IN-SPEC |
| **Team leader** | Ing. William Brach |
| **Industrial/academic partner** | – |
| **Related courses** | Neural Networks, Knowledge Discovery, Information Retrieval, Information Systems Architecture, Data Visualization |

## Mandatory technologies

- OpenAPI 3.x and JSON Schema, validation and a generated mock server
- LLM as Judge
- Python 3.12+
- Docker / Docker Compose, Git, CI (GitHub Actions), automated tests

## Recommended technologies

- Backend: Python 3.12+ with FastAPI
- Grounding and formats for agents: llms.txt / llms-full.txt, AGENTS.md, Model Context Protocol (MCP)
- Input collection: crawler, Markdown/MDX parsers, any DOC
- Evaluation: NLI/entailment models for the soft layer, LLM as a judge only as a last resort; scikit-learn
- Integration: GitHub Action

## Project goals (max. 100 words)

The goal is a service that measures how reliably language models answer questions about a specific software product and how that reliability changes over time. The input is an OpenAPI specification, a changelog, an llms.txt file or a documentation website. From it, the system deterministically generates test tasks and runs them against multiple models in three modes: with no context, with a retrieved snippet, and with the full text embedded. Verifiable claims are checked by running the request against a mock server generated from the same specification. Instead of a single score, the output is a list of questions the models answer incorrectly, the cause of the failure, and how it evolves over time.

## Why should I choose this project (max. 100 words)

You use Codex or Claude Code, and the model confidently suggests a parameter that disappeared from the API a year ago. In this project you will measure this properly. You will build an evaluation system whose results are verified by running code, not by another model's opinion. The outputs are a public leaderboard of documentation for well-known APIs, a long-term dataset of answers that cannot be reconstructed retroactively, and a CI tool.

## Assignment text (max. 500 words)

Developers today ask a language model first, not the documentation. The model answers from training data older than the last three releases of the product. The real cause of the failure is a renamed parameter, a removed field or a changed authentication method, but the error message says nothing about it. The developer loses an hour and the product's maintainer never finds out.

There is currently no way to measure this phenomenon continuously. The goal of the project is to design, implement and validate a service that automatically creates a test suite from documentation, runs it against multiple language models, and repeats the measurement over time. The system consists of the following parts:

- **Input adapters.** An adapter normalizes each input into a corpus of snippets and a set of claims, where each claim carries its own verification method. Hard claims come from the OpenAPI specification and the changelog, medium claims from the llms.txt file, and soft claims from the documentation website. The layers are never averaged together in reports.
- **Deterministic task generation.** The test suite is derived by the system from the claims; it is not invented by a language model. The same input therefore always yields the same tasks, and coverage can be measured.
- **Per-layer verification.** The system verifies hard claims by running the request proposed by the model against a mock server generated from the specification.
- **Repeated runs and diffs.** The system executes runs on a schedule, stores every raw response, compares it with the previous run, and raises an alert when accuracy drops. The CI integration fails the build when a documentation change lowers answer accuracy.
- **Web interface.**

## Resources on the current state of knowledge and technology

- OpenAPI Specification 3.1 and JSON Schema — <https://spec.openapis.org/>
- **Prism** (Stoplight), a mock server generated from the specification. **Schemathesis**, property-based API testing derived from the specification
- **llms.txt** — <https://llmstxt.org/>
- **Model Context Protocol (MCP)** — <https://modelcontextprotocol.io/>
- *When LLMs Lag Behind: Knowledge Conflicts from Evolving APIs in Code Generation.* arXiv:2604.09515
- *LibEvoBench: Probing Temporal Knowledge Stratification in Code Generation Models.* arXiv:2606.25402
- *Lightweight Model Editing for LLMs to Correct Deprecated API Recommendations* (EDAPIBench)
- *Assessing the Capability of LLMs for Deprecated API Usage Updating from Natural Language Descriptions.* ACM TOSEM 2025, doi:10.1145/3808230
- Patil, S. et al.: *Gorilla: Large Language Model Connected with Massive APIs.* arXiv:2305.15334
- *We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs.* arXiv:2406.10279