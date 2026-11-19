"""Stub of the upload API (SPEC §11.1) for testing the Action until role 5's endpoint exists.

    python3 action/stub.py [port] [archive-dir]

Checks the request shape, not the OIDC token. A run is `running` on the first poll and `done`
on the next one. An input containing `<!-- notinspec-mock: fail -->` gives the verdict `fail`;
`input-error` or `internal-error` instead of `fail` ends the run as `error` of that kind.
Standard library only, so CI runs it with the runner's python3.
"""

import io
import json
import re
import sys
import tarfile
from email.parser import BytesParser
from email.policy import default
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

MARKER = re.compile(rb"<!-- notinspec-mock: (fail|input-error|internal-error) -->")
runs: dict[str, dict[str, Any]] = {}


class Stub(BaseHTTPRequestHandler):
    def reply(self, status: int, body: dict[str, object]) -> None:
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:
        if not self.headers.get("Authorization", "").startswith("Bearer "):
            return self.reply(401, {"detail": "missing OIDC token"})
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if self.path == "/api/pr-closed":
            return self.reply(202, {})
        if self.path != "/api/uploads":
            return self.reply(404, {"detail": "not found"})
        head = f"Content-Type: {self.headers['Content-Type']}\r\n\r\n".encode()
        parts = {
            p.get_param("name", header="content-disposition"): p.get_payload(decode=True)
            for p in BytesParser(policy=default).parsebytes(head + body).iter_parts()
        }
        try:
            meta = json.loads(parts["meta"])
            with tarfile.open(fileobj=io.BytesIO(parts["archive"]), mode="r:gz") as tar:
                files = {m.name: f.read() for m in tar if (f := tar.extractfile(m))}
        except (KeyError, ValueError, tarfile.TarError) as exc:
            return self.reply(422, {"detail": f"bad upload: {exc!r}"})
        if meta.get("schema_version") != 0 or "notinspec.yaml" not in files:
            return self.reply(422, {"detail": "bad meta or no notinspec.yaml in the archive"})
        run_id = f"stub-{len(runs) + 1}"
        if len(sys.argv) > 2:  # CI checks what the Action packed
            Path(sys.argv[2], f"{run_id}.tar.gz").write_bytes(parts["archive"])
        marks = {m.decode() for data in files.values() for m in MARKER.findall(data)}
        runs[run_id] = {"polls": 0, "outcome": marks.pop() if marks else "pass"}
        base = f"http://{self.headers['Host']}"
        self.reply(
            202,
            {
                "run_id": run_id,
                "status_url": f"{base}/api/runs/{run_id}",
                "web_url": f"{base}/#/runs/{run_id}",
            },
        )

    def do_GET(self) -> None:
        run = runs.get(self.path.removeprefix("/api/runs/"))
        if run is None:
            return self.reply(404, {"detail": "run not found"})
        run["polls"] += 1
        outcome = run["outcome"] if run["polls"] > 1 else None
        kind = outcome.removesuffix("-error") if outcome and outcome.endswith("-error") else None
        status = "running" if outcome is None else "error" if kind else "done"
        verdict = outcome if status == "done" else None
        self.reply(
            200,
            {
                "schema_version": 0,
                "run_id": self.path.removeprefix("/api/runs/"),
                "status": status,
                "verdict": verdict,
                "comment_md": f"**NOT-IN-SPEC (stub)** {verdict}" if verdict else None,
                "error": f"stub {kind} error" if kind else None,
                "error_kind": kind,
                "web_url": "http://stub/",
            },
        )


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    ThreadingHTTPServer(("127.0.0.1", port), Stub).serve_forever()
