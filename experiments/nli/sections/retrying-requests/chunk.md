## Retrying Requests

urllib3 can automatically retry idempotent requests. This same mechanism also handles redirects. You can control the retries using the `retries` parameter to `request()`. By default, urllib3 will retry requests 3 times and follow up to 3 redirects.

To change the number of retries just specify an integer:

```python
import urllib3

urllib3.request("GET", "https://httpbin.org/ip", retries=10)
```

To disable all retry and redirect logic specify `retries=False`:

```python
import urllib3

urllib3.request(
    "GET",
    "https://nxdomain.example.com",
    retries=False
)
# NewConnectionError

resp = urllib3.request(
    "GET",
    "https://httpbin.org/redirect/1",
    retries=False
)

print(resp.status)
# 302
```

To disable redirects but keep the retrying logic, specify `redirect=False`:

```python
resp = urllib3.request(
    "GET",
    "https://httpbin.org/redirect/1",
    redirect=False
)

print(resp.status)
# 302
```

For more granular control you can use a `Retry` instance. This class allows you far greater control of how requests are retried.

For example, to do a total of 3 retries, but limit to only 2 redirects:

```python
urllib3.request(
    "GET",
    "https://httpbin.org/redirect/3",
    retries=urllib3.Retry(3, redirect=2)
)
# MaxRetryError
```

You can also disable exceptions for too many redirects and just return the `302` response:

```python
resp = urllib3.request(
    "GET",
    "https://httpbin.org/redirect/3",
    retries=urllib3.Retry(
        redirect=2,
        raise_on_redirect=False
    )
)

print(resp.status)
# 302
```

If you want all requests to be subject to the same retry policy, you can specify the retry at the `PoolManager` level:

```python
import urllib3

http = urllib3.PoolManager(retries=False)

http = urllib3.PoolManager(
    retries=urllib3.Retry(5, redirect=2)
)
```

You can still override this pool-level retry policy by specifying `retries` to `request()`.
