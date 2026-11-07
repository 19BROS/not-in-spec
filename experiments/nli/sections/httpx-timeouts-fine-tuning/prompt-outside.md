You are helping to test a documentation-quality tool. The tool extracts claims from one section of software documentation and must reject any claim that the section's prose does not state. Your job is to write realistic claims that it should reject.

## Section

Project: httpx
Location in the docs: Advanced > Timeouts > Fine tuning the configuration

<section>
### Fine tuning the configuration

HTTPX also allows you to specify the timeout behavior in more fine grained detail.

There are four different types of timeouts that may occur. These are connect, read, write, and pool timeouts.

- The connect timeout specifies the maximum amount of time to wait until a socket connection to the requested host is established. If HTTPX is unable to connect within this time frame, a `ConnectTimeout` exception is raised.

- The read timeout specifies the maximum duration to wait for a chunk of data to be received (for example, a chunk of the response body). If HTTPX is unable to receive data within this time frame, a `ReadTimeout` exception is raised.

- The write timeout specifies the maximum duration to wait for a chunk of data to be sent (for example, a chunk of the request body). If HTTPX is unable to send data within this time frame, a `WriteTimeout` exception is raised.

- The pool timeout specifies the maximum duration to wait for acquiring a connection from the connection pool. If HTTPX is unable to acquire a connection within this time frame, a `PoolTimeout` exception is raised. A related configuration here is the maximum number of allowable connections in the connection pool, which is configured by the `limits` argument.

You can configure the timeout behavior for any of these values...

```python
# A client with a 60s timeout for connecting, and a 10s timeout elsewhere.
timeout = httpx.Timeout(10.0, connect=60.0)
client = httpx.Client(timeout=timeout)

response = client.get('http://example.com/')
```
</section>

## Task

Write 6 claims about httpx that a careless claim extractor could plausibly produce from this section, but that the section's **prose** does **not** state:

- 3 claims that are **true for the real httpx** (from your own knowledge, from another part of its documentation, or only visible in the code blocks) but are not stated in the prose of this section.
- 3 claims that **sound like they come from this section** but subtly go beyond it: an over-generalisation, a stronger or weaker qualifier ("always" for "can", "only" added or dropped), a cause or purpose the text does not give, or a detail merged from two different sentences in a way the text does not say.

Do not write claims that contradict the section outright (no changed numbers, no plain negations). Those are covered elsewhere.

Each claim must look like a normal extractor output: atomic, self-contained (name the subject explicitly), one sentence, no hedging. For each claim give a **citation**: the shortest span of the section's prose that the claim would most plausibly be attributed to, copied character for character (keep backticks and punctuation, fix nothing, no "..."). Add `"kind": "outside"` for the first group and `"kind": "beyond"` for the second.

## Output

Return only the JSON object inside one ```json code block, with no text before or after it. It must be valid JSON: use only straight ASCII quotes (`"` and `'`), never typographic quotes such as “ ” ‘ ’, also inside claims (write `httpx's`, not `httpx’s`).

```json
{"claims": [{"id": "o1", "claim": "...", "citation": "...", "type": "fact", "kind": "outside"}]}
