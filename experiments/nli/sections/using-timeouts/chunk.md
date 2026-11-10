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
