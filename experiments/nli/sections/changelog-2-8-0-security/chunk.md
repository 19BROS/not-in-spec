### Security

Fixed the following security issues:

- The TLS configuration for HTTPS proxies could be ignored or overridden. (High severity, GHSA-8988-9cw3-xx77)

- `HTTPResponse.stream()` and `read_chunked()` could buffer a chunk-size line of unbounded length in memory. (High severity, GHSA-vxq7-64xx-v4gw)

- Chunked Deflate streaming could enter an infinite loop. (Medium severity, GHSA-gh4c-6fx4-qh6g)

> **Caution:** urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. Configurations relying on that behavior may require changes.
>
> Configure proxy CA certificates and client certificates in `proxy_ssl_context`, and proxy identity checks with `proxy_assert_hostname` or `proxy_assert_fingerprint`. Destination client certificates and identity overrides no longer apply to HTTPS forwarding proxy connections.
