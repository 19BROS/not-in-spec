#!/usr/bin/env sh
# Smoke test of the mock service on a running stack (CI job `compose`, SPEC §12). From the repo root.
set -eu
c="docker compose -f deploy/docker-compose.yml"
spec=deploy/fixtures/openapi.yaml
# a relative path, so a Windows `docker compose cp` finds it too
other=deploy/mock/.smoke-other.yaml
trap 'rm -f "$other"' EXIT
# another spec, whose operation defines its own 400
{ cat "$spec"; echo '        "400": { description: Bad id, content: { application/json: { example: { error: bad id } } } }'; } > "$other"
# the worker stores uploaded specs by content hash, like this
for f in "$spec" "$other"; do
  $c cp "$f" "worker:/specs/$(sha256sum "$f" | cut -d' ' -f1).yaml"
done

$c exec -T worker python - "$(sha256sum "$spec" | cut -d' ' -f1).yaml" \
  "$(sha256sum "$other" | cut -d' ' -f1).yaml" <<'EOF'
import json, sys, urllib.error, urllib.request

def call(url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data, {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, response.read(), response.headers
    except urllib.error.HTTPError as error:
        return error.code, error.read(), error.headers

status, body, _ = call("http://mock:4011/serve", {"spec": sys.argv[1]})
assert status == 200, body
base = json.loads(body)["base_url"]
status, _, headers = call(f"{base}/pets/1")
assert status == 200 and "sl-violations" not in headers
# no 4xx in the spec: Prism's own 422 problem with a validation list (SPEC §12)
status, body, _ = call(f"{base}/pets/abc")
assert status == 422 and json.loads(body)["validation"], "Prism must reject a request the spec forbids"
assert call("http://mock:4011/serve", {"spec": "../../etc/passwd"})[0] == 422
# another spec gets another port: the old base_url refuses instead of answering for it
status, body, _ = call("http://mock:4011/serve", {"spec": sys.argv[2]})
assert status == 200 and json.loads(body)["base_url"] != base, body
# the spec defines a 400: Prism answers with it and lists the violations in sl-violations
status, _, headers = call(f"{json.loads(body)['base_url']}/pets/abc")
assert status == 400 and json.loads(headers["sl-violations"]), (status, dict(headers))
try:
    call(f"{base}/pets/1")
    raise AssertionError("the replaced Prism still answers")
except urllib.error.URLError:
    pass
print("mock ok: serves the spec, validates requests, rejects paths, new port per spec")
EOF

# sandbox is an internal network: nothing in the mock reaches the internet
if $c exec -T mock wget -q -T 5 -O /dev/null https://example.com; then
  echo "mock reached the internet"; exit 1
fi
echo "mock ok: no internet"
