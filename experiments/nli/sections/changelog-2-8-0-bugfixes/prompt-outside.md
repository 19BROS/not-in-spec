You are helping to test a documentation-quality tool. The tool extracts claims from one section of software documentation and must reject any claim that the section's prose does not state. Your job is to write realistic claims that it should reject.

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
