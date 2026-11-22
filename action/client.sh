#!/usr/bin/env bash
# Thin client of our service (SPEC §11.1): pack, upload with OIDC, poll, write the comment.
# Writes outputs code (0 pass or no result, 1 fail, 2 error), verdict, run-url, comment.
# Our outage never fails the caller's job; their wrong setup does.
set -uo pipefail

out="$RUNNER_TEMP/notinspec"
mkdir -p "$out"
comment="$out/comment.md"
server="${SERVER_URL%/}"

finish() { # code verdict text
  printf '<!-- notinspec -->\n%s\n' "$3" > "$comment"
  cat "$comment" >> "$GITHUB_STEP_SUMMARY"
  { echo "code=$1"; echo "verdict=$2"; echo "comment=$comment"; } >> "$GITHUB_OUTPUT"
  exit 0
}
setup_error() { echo "::error::NOT-IN-SPEC: $1"; finish 2 "" "**NOT-IN-SPEC** ✗ error: $1"; }
no_result() {
  echo "::warning::NOT-IN-SPEC: $1"
  finish 0 "" "**NOT-IN-SPEC** ⚠ no result: $1. This does not block the PR."
}

case "$server" in
  https://*|http://localhost:*|http://127.0.0.1:*) ;;
  *) setup_error "server-url must be https://" ;;
esac
if [ -z "${ACTIONS_ID_TOKEN_REQUEST_URL:-}" ]; then
  setup_error "no OIDC token: give the job \`permissions: id-token: write\`"
fi
# a fixed audience, not our URL: moving the service never breaks registered workflows (SPEC §11.1)
token=$(curl -fsS --retry 3 -H "Authorization: Bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
  "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=notinspec" | jq -r .value) ||
  setup_error "could not get an OIDC token from GitHub"

post() { # path, then curl args; prints the HTTP status, body in $out/response.json
  local path=$1; shift
  # retried POSTs are safe: the API returns the same run for the same (run_id, run_attempt)
  curl -sS --max-time 120 --retry 3 -o "$out/response.json" -w '%{http_code}' \
    -H "Authorization: Bearer $token" "$@" "$server$path"
}
detail() { jq -r '.detail // empty' "$out/response.json" 2>/dev/null || true; }

if [ "$EVENT_ACTION" = closed ]; then
  status=$(post /api/pr-closed -X POST) || status=000
  case "$status" in
    2??) echo "NOT-IN-SPEC: closed PR reported" ;;
    *) echo "::warning::NOT-IN-SPEC: could not report the closed PR (HTTP $status) $(detail)" ;;
  esac
  exit 0
fi

head_sha=null base_sha=null
if [ -n "$HEAD_SHA" ]; then
  head_sha="\"$HEAD_SHA\""
  # the merge commit's first parent finds the baseline main run (SPEC §7)
  base=$(git rev-parse HEAD^1 2>/dev/null) ||
    setup_error "check out with \`fetch-depth: 2\`, the run needs the merge commit's first parent"
  base_sha="\"$base\""
fi
printf '{"schema_version": 0, "head_sha": %s, "base_sha": %s}\n' "$head_sha" "$base_sha" > "$out/meta.json"

# input selection is core's, the same code the server runs on the archive; --frozen: the
# versions in our uv.lock, so a new release of a dependency never changes the Action
if ! uv run --frozen --no-dev --project "$GITHUB_ACTION_PATH/.." --package notinspec \
  notinspec pack --config "$CONFIG" --out "$out/inputs.tar.gz" 2> "$out/pack-stderr.txt"; then
  cat "$out/pack-stderr.txt" >&2
  setup_error "$(tail -n 1 "$out/pack-stderr.txt")"
fi

status=$(post /api/uploads -F "archive=@$out/inputs.tar.gz;type=application/gzip" \
  -F "meta=@$out/meta.json;type=application/json") || status=000
case "$status" in
  200|202) ;;
  429) no_result "our service is busy (HTTP 429), try again later" ;;
  4??) setup_error "upload rejected (HTTP $status): $(detail)" ;;
  *) no_result "our service did not accept the upload (HTTP $status)" ;;
esac
status_url=$(jq -r .status_url "$out/response.json")
run_url=$(jq -r .web_url "$out/response.json")
echo "run-url=$run_url" >> "$GITHUB_OUTPUT"
echo "NOT-IN-SPEC run: $run_url"

deadline=$(( $(date +%s) + TIMEOUT_MINUTES * 60 ))
while :; do
  # a failed poll is retried until the deadline: a deploy restarts the API for a few seconds
  if curl -fsS --max-time 30 -o "$out/run.json" "$status_url"; then
    case "$(jq -r .status "$out/run.json")" in
      done|error) break ;;
      *) echo "NOT-IN-SPEC: $(jq -r .status "$out/run.json")" ;;
    esac
  fi
  [ "$(date +%s)" -lt "$deadline" ] || no_result "the run did not finish in $TIMEOUT_MINUTES minutes, see $run_url"
  sleep 15
done

text=$(jq -r '.comment_md // empty' "$out/run.json")
if [ "$(jq -r .status "$out/run.json")" = error ]; then
  error=$(jq -r '.error // "unknown error"' "$out/run.json")
  # only the caller's inputs fail their job; our crash (any other error_kind) never does
  [ "$(jq -r .error_kind "$out/run.json")" = input ] || no_result "the run failed on our side ($error), see $run_url"
  echo "::error::NOT-IN-SPEC run failed: $error"
  finish 2 "" "${text:-**NOT-IN-SPEC** ✗ error: $error}"
fi
verdict=$(jq -r .verdict "$out/run.json")
case "$verdict" in
  pass) finish 0 pass "$text" ;;
  fail) echo "::error::NOT-IN-SPEC: documentation change lowers usage, see $run_url"; finish 1 fail "$text" ;;
  null) no_result "no verdict yet, see $run_url" ;;
  *) no_result "our service returned an unknown verdict: $verdict" ;;
esac
