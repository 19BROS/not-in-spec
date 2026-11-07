### Configuring Exponential Backoff

By default, `Retry` does not sleep between retry attempts (`backoff_factor=0`), though it will still respect delays requested by the server when a response includes a `Retry-After` header (see `respect_retry_after_header`). In production systems, retrying immediately without backoff can overwhelm a recovering server or quickly exhaust API rate limits.

When no server-requested delay is applied, you can set a non-zero `backoff_factor` to introduce exponential delays between retries. The sleep delay is calculated using the formula:

```
{backoff factor} * (2 ** ({number of previous retries}))
```

seconds, with no delay before the second attempt (the first retry) because most transient errors resolve immediately. For example, a `backoff_factor` of `0.5` yields retry sleeps of `0.0s`, `1.0s`, `2.0s`, etc., up to `backoff_max`:

```python
import urllib3

# Retries wait 0.0s (immediate 2nd attempt), 1.0s, and 2.0s (plus jitter)
retries = urllib3.Retry(
    total=3,
    backoff_factor=0.5,
    backoff_jitter=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
)
http = urllib3.PoolManager(retries=retries)
```

Adding `backoff_jitter` introduces random variance to avoid the "thundering herd" problem where many clients retry in lockstep against a server.
