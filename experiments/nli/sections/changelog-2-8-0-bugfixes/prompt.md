You are a claim extractor for a documentation-quality tool. You read one section of software documentation and list the atomic facts its prose states about the software.

## Section

Project: urllib3
Location in the docs: Changelog > 2.8.0 (2026-09-15) > Bugfixes

<section>
### Bugfixes

- Fixed response header handling to replace obsolete folded header lines (`obs-fold`) with spaces in accordance with RFC 9112, preventing raw CRLF sequences from appearing in header values such as `Set-Cookie`.

- Fixed usage of `proxy_ssl_context` with `ProxyManager` when `use_forwarding_for_https=True`. Passing `ssl_context` instead of `proxy_ssl_context` for HTTPS proxies in this configuration now emits a `FutureWarning` and will raise an error in v3.0.

- Changed behavior of the default `ConnectionPool.pool` initialization. `LifoQueue` is now resolved from the `queue` module after the `ConnectionPool` is instantiated instead of using the default cached `QueueCls` class property. This is done because sometimes the `queue.LifoQueue` is monkey-patched late in the program, such as by gevent.

- Raised `UnrewindableBodyError` instead of `ValueError` when retrying a request whose body had `tell()` but not `seek()`.

- Decoded percent-encoded SOCKS proxy credentials before authenticating with the proxy server.

- Fixed `HTTPResponse.drain_conn()` to discard unread response data in 64 KiB chunks (same as the default `amt` when doing `HTTPResponse.stream(...)`).

- Fixed `is_ipaddress()` to detect non-standard IPv4 forms accepted by `socket.connect`, such as hex (`0x7f000001`), octal (`0177.0.0.1`), and decimal integers (`2130706433`), ensuring SSL certificate verification uses the correct mode for these addresses.

- Fixed `HTTPConnectionPool.urlopen` raising a misleading `FullPoolError` instead of `ValueError` when called with an invalid `timeout` argument on a pool created with `block=True`.

- Fixed port-zero handling to preserve explicit `:0` values instead of substituting the default ports 80 or 443 in URL parsing, pool selection, proxy configuration, `connection_from_url()`, and HTTP/2 request authority.

- Fixed a bug where `PoolManager` passed the `assert_hostname` and `assert_fingerprint` parameters to HTTP connection pools.

- Fixed `HTTPConnectionPool.urlopen()` and HTTP proxy forwarding to strip URL fragments from absolute request targets before sending requests.

- Added safeguards to the proxy tunneling code to prevent potential security issues when handling invalid characters in the proxy host and HTTP headers. This change affects users of Python 3.10, Python 3.11, and Python 3.12 when the standard library does not contain the fix; those on newer Python versions should upgrade to 3.13.14+ or 3.14.5+ to get the same security fixes.

- Fixed `HTTPSConnection.connect()` overriding `ProxyConfig.ssl_context`'s certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy.

  `HTTPSConnection` no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes and continues to use its `ssl_context` as a fallback when an HTTPS proxy forwards an HTTP target.

- Fixed URL parsing to more strictly enforce RFC 3986 host syntax, rejecting invalid host input such as raw spaces and control characters, malformed percent-encodings, and percent-encoded control characters in HTTP(S) hosts and IPv6 zone identifiers, including proxy CONNECT tunnel targets. Host normalization now also follows RFC 3986 normalization rules for percent-encoded octets by decoding percent-encoded unreserved characters and uppercasing the hexadecimal digits of retained percent-encoded octets.

- Fixed an `AttributeError` on Python built with OpenSSL 4+, where `ssl.PROTOCOL_TLSv1` no longer exists.

- Fixed `urllib3.contrib.pyopenssl` to use cryptography APIs when reading a certificate subject and loading encrypted private keys, avoiding `DeprecationWarning` raised by pyOpenSSL 26.3.0+.

- Fixed handling of HTTP 303 redirects for requests with chunked or file-like bodies.

- Fixed `assert_fingerprint()` to raise `SSLError` instead of `binascii.Error` when a fingerprint has a supported length but contains non-hexadecimal characters.
</section>

## What a claim is

A claim is one atomic, self-contained statement of fact that the **prose** of the section makes about the software: behaviour, defaults, units, value ranges, allowed values, what a parameter or option does, when an error is raised, what changed between versions.

## Rules

1. **Atomic.** One fact per claim. "retries 3 times and follows up to 3 redirects" is two claims.
2. **Self-contained.** A claim must be understandable without the section. Name the subject explicitly (library, class, function, parameter). No "it", "this", "the class", "the parameter". Use the location in the docs to resolve what the section is about.
3. **Faithful.** State only what the prose says. Add nothing from your own knowledge of the software, do not generalise, and do not weaken or strengthen the statement. Keep qualifiers ("can", "by default", "up to", "only"), negations, numbers and units exactly.
4. **Prose only.** Code blocks are shown for context only. A fact that appears only in code or in a code comment is not a claim.
5. **Citation.** For every claim, copy the shortest contiguous span of the section's prose that supports it, character for character: keep backticks, punctuation and spelling, fix nothing, no "...". It may be part of a sentence but must contain the evidence.
6. **Type.** `change` if the claim says something was added, removed, renamed, replaced or deprecated in some version; otherwise `fact`.
7. **Skip** navigation and lead-ins ("see X", "for example:", "the following code"), opinions and marketing. An instruction that implies a fact *is* a claim: "To disable redirects, specify `redirect=False`" → "Passing redirect=False disables redirects."
8. No duplicates.

## Example (a different project)

Section prose: "`connect()` accepts an optional `timeout` parameter in seconds, default 30. Since 2.0, `retries` is replaced by the new `retry_policy`."

```json
{"claims": [
  {"id": "c1", "claim": "The timeout parameter of connect() is optional.", "citation": "`connect()` accepts an optional `timeout` parameter", "type": "fact"},
  {"id": "c2", "claim": "The timeout parameter of connect() is given in seconds.", "citation": "`timeout` parameter in seconds", "type": "fact"},
  {"id": "c3", "claim": "The default value of the timeout parameter of connect() is 30 seconds.", "citation": "in seconds, default 30", "type": "fact"},
  {"id": "c4", "claim": "Since version 2.0, the retries parameter is replaced by the retry_policy parameter.", "citation": "Since 2.0, `retries` is replaced by the new `retry_policy`", "type": "change"}
]}
```

## Output

Return only the JSON object inside one ```json code block, with no text before or after it. It must be valid JSON: use only straight ASCII quotes (`"` and `'`), never typographic quotes such as “ ” ‘ ’, also inside claims (write `urllib3's`, not `urllib3’s`).

```json
{"claims": [{"id": "c1", "claim": "...", "citation": "...", "type": "fact"}]}
```
