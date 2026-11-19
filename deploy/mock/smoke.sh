#!/usr/bin/env sh
# Smoke test of the mock service on a running stack (CI job `compose`, SPEC §12). From the repo root.
set -eu
c="docker compose -f deploy/docker-compose.yml"
spec=deploy/fixtures/openapi.yaml
# a relative path, so a Windows `docker compose cp` finds it too
other=deploy/mock/.smoke-other.yaml
trap 'rm -f "$other"' EXIT
{ cat "$spec"; echo "# another spec"; } > "$other"
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
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()

status, body = call("http://mock:4011/serve", {"spec": sys.argv[1]})
assert status == 200, body
base = json.loads(body)["base_url"]
assert call(f"{base}/pets/1")[0] == 200
assert call(f"{base}/pets/abc")[0] == 422, "Prism must reject a request the spec forbids"
assert call("http://mock:4011/serve", {"spec": "../../etc/passwd"})[0] == 422
# another spec gets another port: the old base_url refuses instead of answering for it
status, body = call("http://mock:4011/serve", {"spec": sys.argv[2]})
assert status == 200 and json.loads(body)["base_url"] != base, body
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
