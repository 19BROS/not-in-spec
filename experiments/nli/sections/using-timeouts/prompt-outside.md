You are helping to test a documentation-quality tool. The tool extracts claims from one section of software documentation and must reject any claim that the section's prose does not state. Your job is to write realistic claims that it should reject.

## Section

Project: urllib3
Location in the docs: User Guide > Using Timeouts

<section>
## Using Timeouts

Timeouts allow you to control how long (in seconds) requests are allowed to run before being aborted. In simple cases, you can specify a timeout as a `float` to `request()`:

```python
import urllib3

resp = urllib3.request(
    "GET",
    "https://httpbin.org/delay/3",
    timeout=4.0
)

print(type(resp))
# <class "urllib3.response.HTTPResponse">

# This request will take more time to process than timeout.
urllib3.request(
    "GET",
    "https://httpbin.org/delay/3",
    timeout=2.5
)
# MaxRetryError caused by ReadTimeoutError
```

For more granular control you can use a `Timeout` instance which lets you specify separate connect and read timeouts:

```python
import urllib3

resp = urllib3.request(
    "GET",
    "https://httpbin.org/delay/3",
    timeout=urllib3.Timeout(connect=1.0)
)

print(type(resp))
# <urllib3.response.HTTPResponse>

urllib3.request(
    "GET",
    "https://httpbin.org/delay/3",
    timeout=urllib3.Timeout(connect=1.0, read=2.0)
)
# MaxRetryError caused by ReadTimeoutError
```

If you want all requests to be subject to the same timeout, you can specify the timeout at the `PoolManager` level:

```python
import urllib3

http = urllib3.PoolManager(timeout=3.0)

http = urllib3.PoolManager(
    timeout=urllib3.Timeout(connect=1.0, read=2.0)
)
```

You still override this pool-level timeout by specifying `timeout` to `request()`.
</section>

## Task

Write 6 claims about urllib3 that a careless claim extractor could plausibly produce from this section, but that the section's **prose** does **not** state:

- 3 claims that are **true for the real urllib3** (from your own knowledge, from another part of its documentation, or only visible in the code blocks) but are not stated in the prose of this section.
- 3 claims that **sound like they come from this section** but subtly go beyond it: an over-generalisation, a stronger or weaker qualifier ("always" for "can", "only" added or dropped), a cause or purpose the text does not give, or a detail merged from two different sentences in a way the text does not say.

Do not write claims that contradict the section outright (no changed numbers, no plain negations). Those are covered elsewhere.

Each claim must look like a normal extractor output: atomic, self-contained (name the subject explicitly), one sentence, no hedging. For each claim give a **citation**: the shortest span of the section's prose that the claim would most plausibly be attributed to, copied character for character (keep backticks and punctuation, fix nothing, no "..."). Add `"kind": "outside"` for the first group and `"kind": "beyond"` for the second.

## Output

Return only the JSON object inside one ```json code block, with no text before or after it. It must be valid JSON: use only straight ASCII quotes (`"` and `'`), never typographic quotes such as “ ” ‘ ’, also inside claims (write `urllib3's`, not `urllib3’s`).

```json
{"claims": [{"id": "o1", "claim": "...", "citation": "...", "type": "fact", "kind": "outside"}]}
