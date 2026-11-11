---
title: Acme client
sidebar_position: 2
---

The Acme Python client wraps the Acme Payments REST API.

# Client

## Connecting

`connect()` accepts an optional `timeout` parameter in seconds, default 30.
Since 2.0, `retries` is replaced by the new `retry_policy`.

Example:

```python
# create a client and connect
conn = client.connect(timeout=10, retry_policy=RetryPolicy(max_attempts=3))
```

### Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `timeout` | `int` | `30` | seconds to wait for the connection |
| `retry_policy` | `RetryPolicy` | `None` | how to retry failed attempts |

### Example

1. Install the package:

   ```sh
   pip install acme
   ```

2. Connect with a short timeout.

## Charges

### Example

```bash
curl -X POST https://api.acme.test/v1/charges \
  -H "Authorization: Bearer $ACME_KEY" \
  -d amount=1000 -d currency=eur
```

> **Note:** amounts are in cents.

Errors
------

The client raises `AcmeError` for every non-2xx response.

<div class="callout">Rate limits apply.</div>
