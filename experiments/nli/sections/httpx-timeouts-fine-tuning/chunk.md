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
