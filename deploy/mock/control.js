// Control endpoint of the `mock` service (SPEC §12): the worker asks it to serve one spec,
// so the worker never needs the Docker socket. Runs in the stoplight/prism image, Node stdlib only.
//   POST :4011/serve {"spec": "<sha256>.yaml"} -> 200 {"base_url": "http://mock:<port>"} | 4xx {"detail"}
//     422: Prism rejected the spec (the user's problem); 503: Prism could not run (ours)
//   GET  :4011/health -> 200 {"serving": "<name>" | null} | 503 when the image has no Prism CLI
"use strict";
const http = require("node:http");
const net = require("node:net");
const fs = require("node:fs");
const { spawn } = require("node:child_process");

const SPECS = "/specs"; // written by the worker, read-only here
const NAME = /^[0-9a-f]{64}\.(json|ya?ml)$/; // a content hash, so never a path
const CLI = "/usr/src/prism/packages/cli/dist/index.js"; // moves with the image version

// shortcut: one Prism at a time, a new spec replaces the old one; when runs check several
// specs at once, keep one Prism per spec
let current = null; // { name, child, port, ready, exited, log }
let switches = 0;
let queue = Promise.resolve(); // switches never overlap

async function stop() {
  const run = current;
  current = null;
  if (!run || run.exited) return;
  const exited = new Promise((resolve) => run.child.once("exit", resolve));
  run.child.kill("SIGTERM");
  const killer = setTimeout(() => run.child.kill("SIGKILL"), 5000); // busy on a hostile schema
  await exited;
  clearTimeout(killer);
}

function portOpen(port) {
  return new Promise((resolve) => {
    const socket = net.connect(port, "127.0.0.1", () => {
      socket.end();
      resolve(true);
    });
    socket.once("error", () => resolve(false));
  });
}

async function serve(name) {
  if (current && current.name === name && current.ready && !current.exited) return current.port;
  await stop();
  // a new port per switch: a run still holding the old base_url gets "connection refused",
  // never answers validated against another spec
  const port = 4100 + (switches++ % 1000);
  // multiprocess mode crashes in the container (cluster.isPrimary undefined)
  const child = spawn("node", [
    CLI, "mock", "-h", "0.0.0.0", "-p", String(port), "--multiprocess=false", `${SPECS}/${name}`,
  ]);
  const run = { name, child, port, ready: false, exited: false, log: "" };
  const keep = (data) => { run.log = (run.log + data).slice(-2000); };
  child.stdout.on("data", keep);
  child.stderr.on("data", (data) => { keep(data); process.stderr.write(data); });
  // killed by a signal (OOM under mem_limit) is our failure, not the spec's
  child.once("exit", (code, signal) => { run.exited = true; run.ours ||= signal !== null; });
  // spawn can fail (EAGAIN under the memory limit); without a listener it kills this server
  child.once("error", (error) => { keep(String(error)); run.exited = true; run.ours = true; });
  current = run;
  for (let waited = 0; waited < 30000; waited += 200) {
    if (run.exited) {
      current = null;
      if (run.ours) throw failure(503, `Prism could not run: ${run.log.trim()}`);
      throw failure(422, `Prism stopped on this spec: ${run.log.trim()}`);
    }
    if (await portOpen(port)) {
      run.ready = true;
      return port;
    }
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  await stop();
  throw failure(503, "Prism did not start in 30 s");
}

function failure(status, message) {
  return Object.assign(new Error(message), { status });
}

function reply(res, status, body) {
  res.writeHead(status, { "Content-Type": "application/json" }).end(JSON.stringify(body));
}

http.createServer((req, res) => {
  if (req.method === "GET" && req.url === "/health") {
    // fails the deploy's `up --wait` when a new image moved the CLI, instead of every /serve
    if (!fs.existsSync(CLI)) return reply(res, 503, { detail: `no Prism CLI at ${CLI}` });
    return reply(res, 200, { serving: current && current.ready && !current.exited ? current.name : null });
  }
  if (req.method !== "POST" || req.url !== "/serve") return reply(res, 404, { detail: "not found" });
  let body = "";
  req.on("data", (data) => {
    body += data;
    if (body.length > 1000) {
      reply(res, 413, { detail: "body over 1000 bytes" });
      req.destroy();
    }
  });
  req.on("end", () => {
    let name;
    try { name = JSON.parse(body).spec; } catch { return reply(res, 400, { detail: "body is not JSON" }); }
    if (typeof name !== "string" || !NAME.test(name)) {
      return reply(res, 422, { detail: "spec must be <sha256>.json or .yaml" });
    }
    if (!fs.existsSync(`${SPECS}/${name}`)) return reply(res, 404, { detail: `no ${name} in ${SPECS}` });
    queue = queue.then(() => serve(name)).then(
      (port) => reply(res, 200, { base_url: `http://mock:${port}` }),
      (error) => reply(res, error.status || 503, { detail: error.message }),
    );
  });
}).listen(4011, "0.0.0.0");
