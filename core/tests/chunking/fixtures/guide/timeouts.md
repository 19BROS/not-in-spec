---
title: Timeouts and retries
---

Strand is a small HTTP client for Python. This page explains how it waits and when it tries again.

# Timeouts and retries

## Timeouts

Every request has a timeout. By default Strand waits 10 seconds for the connection and
30 seconds for the response, i.e. a slow server fails after at most 40 seconds in total.
Pass a `strand.Timeout` object to change that, e.g. `Timeout(connect=2.5, read=60)`.

What happens when the timeout is reached? Strand raises `strand.TimeoutError` and closes
the connection. The error is never retried unless you enable retries (see [Retries](#retries)).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `connect` | `float` | `10.0` | seconds to wait for the TCP and TLS handshake |
| `read` | `float` | `30.0` | seconds to wait between two bytes of the response |
| `total` | `float \| None` | `None` | upper bound for the whole request; `None` means no bound |

Example:

```python
import strand

# wait at most 2.5 s for the connection. A slow server is fine.
client = strand.Client(timeout=strand.Timeout(connect=2.5, read=60))
```

A timeout of `0` is not allowed and raises `ValueError`. Use `None` to wait forever, which
is almost never what you want in production.

## Retries

Strand retries a request only when all of these hold:

- the method is idempotent (`GET`, `HEAD`, `PUT`, `DELETE`, `OPTIONS`). `POST` is never
  retried automatically.
- the error is a connection error or one of the status codes 502, 503 and 504.
- fewer than `retries` attempts have been made. The default is 3.
- for a status code, the response arrived within the read timeout:

  ```python
  client = strand.Client(retries=strand.Retry(total=5, status=[429, 503]))
  ```

> **Note:** a retried request is sent again from scratch. Request bodies passed as a
> generator can't be replayed, so Strand raises `strand.StreamConsumedError` instead.
>
> Use bytes or a file object when you need retries.

### Backoff

Between two attempts Strand sleeps `backoff_factor * 2 ** (attempt - 1)` seconds. With the
default factor of 0.5 that is approx. 0.5 s, 1 s and 2 s. The sleep never exceeds
`Retry.max_backoff`, which is 120 seconds by default.

If the server sends a `Retry-After` header, Strand waits that long instead. Values over
`max_backoff` are capped. Set `respect_retry_after=False` to ignore the header.

## Migrating from 1.x

Version 2.0 changed several names. The old names were deprecated in 1.8 and removed in 2.0.

1. `max_retries` was renamed to `retries`. It now accepts an `int` or a `strand.Retry`.
2. `Retry(method_whitelist=...)` was renamed to `Retry(allowed_methods=...)`.
3. `Timeout.total` used to default to 60 seconds. It now defaults to `None`.
4. `strand.ConnectTimeout` and `strand.ReadTimeout` were merged into `strand.TimeoutError`.

If you catch the old exceptions, catch `strand.TimeoutError` instead. Code that set
`max_retries=0` to turn retries off should now pass `retries=False`. Passing `0` still
works but logs a warning.

The 1.x behaviour of retrying `POST` on connection errors was removed. It could send a
payment twice. If you really need it, add `POST` to `allowed_methods` yourself.

Before:

```python
client = strand.Client(max_retries=strand.Retry(method_whitelist={"GET", "POST"}))
```

After:

```python
client = strand.Client(retries=strand.Retry(allowed_methods={"GET", "POST"}))
```

See the [changelog](https://example.org/strand/changelog) for the full list of changes.
