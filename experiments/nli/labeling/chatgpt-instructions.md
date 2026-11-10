You are annotating data for an evaluation of documentation-grounding checks. Work only from the section text below. Do not use your own knowledge of {{PROJECT}}.

## Task

For each claim, decide whether the **prose** of this documentation section supports it. Read the section as part of the {{PROJECT}} documentation, at the location `{{BREADCRUMB}}`, so a claim may name {{PROJECT}}, the class or the function the section is about even if the sentence itself does not.

- `entailment`: the prose states the claim, or it follows directly from the prose (a faithful paraphrase is fine).
- `neutral`: the prose does not state it. This includes claims that may well be true but are not written here, claims that only appear in a code block or code comment, and claims that generalise, strengthen, weaken or drop a qualifier ("can", "by default", "only", "up to") or a number/unit.
- `contradiction`: the prose states the opposite or a different value.

Code blocks are shown only for context. A fact found only in code is `neutral`.
The citation is the span the claim's author pointed at. Use it to find the place, but judge the claim against the whole section.
Set `borderline` to true when you are genuinely unsure.

## Section ({{BREADCRUMB}})

<section>
{{SECTION}}
</section>

## Claims ({{COUNT}})

```json
{{CLAIMS}}
```

## Output

Return only one ```json code block with exactly {{COUNT}} objects, in the same order, with no text before or after it:

```json
[{"id": "q123", "verdict": "entailment", "borderline": false}]
```
