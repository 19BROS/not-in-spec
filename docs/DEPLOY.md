# NOT-IN-SPEC — Deployment runbook

How production runs, and what to do when something breaks. For the design behind it, see [SPEC.md §8](SPEC.md#8-devops).

## At a glance

| | |
|---|---|
| Site | https://147-175-151-17.sslip.io (API: `/api/health`) — **public**: 80 and 443 reachable from the internet, SSH (22) only from the STU network / VPN (checked 2026-11-05 from outside STU). [sslip.io](https://sslip.io) resolves the name to the IP, so Let's Encrypt can issue a cert without our own domain. |
| VM | OpenStack project `fiit-tp2026-team19`, instance `notinspec`, Ubuntu 24.04, 4 vCPU / 16 GB |
| Login | `ssh notinspec` with the SSH config below (key-only, `ubuntu` has passwordless sudo) |
| Expires | **2027-06-30** — request an extension from FIIT before then, or the VM is blocked and later deleted |
| Open ports (FIIT firewall) | 22, 80, 443, 3389, 5432, 8000–10000 |

Add this to `~/.ssh/config` (Windows: `C:\Users\<you>\.ssh\config`) so `ssh notinspec` just works:

```
Host notinspec
    HostName 147.175.151.17
    User ubuntu
    IdentityFile ~/.ssh/fiit_vm
```

`IdentityFile` is whichever private key the VM knows for you (see *Giving a teammate SSH access*).

## How a deploy happens

Nobody deploys by hand. Merging a PR into `main` does it:

1. `CI` runs on the push to `main`: lint, tests, Compose smoke test, then pushes `api`, `worker`, `web`, `cli` images to GHCR tagged with the commit SHA.
2. When CI succeeds, `Deploy` runs on the **self-hosted runner on the VM** (label `notinspec-deploy`, environment `production`).
3. It checks out that commit, pulls the images for that SHA, makes sure the NLI model is on its volume (see *NLI model* below) and runs `docker compose up -d --remove-orphans` with `/opt/notinspec/.env`: every service of that commit's compose file starts (plus the `backup` profile), and services it no longer has are stopped.
4. Before that `up`, the deploy runs the one-shot `migrate` service, and `api` and `worker` start only after it exits 0 (see *Database* below).

Pull requests, forks included, never run on the VM.

## What lives where on the VM

| Path | What |
|---|---|
| `/data` | 60 GB data volume (`vdb`, label `notinspec-data`), mounted via `/etc/fstab` |
| `/data/docker` | Docker root: images, containers, **the Postgres volume** |
| `/data/backups` | daily database dumps (see below) |
| `/opt/notinspec/.env` | production secrets (Postgres password, API keys), owned by `deploy`, mode 600. **Never in git.** |
| `/home/deploy/actions-runner` | GitHub Actions runner, systemd service `actions.runner.19BROS-not-in-spec.notinspec-vm` |

The runner runs as user `deploy`: in the `docker` group, no password, no sudo.

## Everyday commands (on the VM, as `ubuntu`)

```sh
sudo docker ps                                    # what is running
sudo docker logs -f --tail 100 notinspec-api-1    # logs of one service (api, worker, web, proxy, postgres, backup)
sudo systemctl status 'actions.runner.*'          # is the runner alive?
sudo systemctl restart 'actions.runner.*'         # restart it
df -h / /data                                     # disk space
```

## Rollback / redeploy

- **Redeploy the current version:** GitHub → Actions → *Deploy* → latest run → *Re-run jobs*.
- **Roll back:** GitHub → Actions → *Deploy* → open an older **successful** run → *Re-run jobs*. It redeploys that run's commit and images.
- Better long-term: revert the bad PR on `main`. That deploys automatically.
- **Not across a migration.** An older commit's `migrate` doesn't know the newer revision and fails, so that deploy changes nothing (old containers keep running). Fix forward with a PR instead.

## NLI model (SPEC §6.4, §12)

The worker scores claims with a local cross-encoder (`MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` at the revision pinned in `core/src/notinspec/nli/local.py`, ~870 MB of weights, ~3 GB peak RAM in fp32). It is not in the image:

- The weights live on the named volume `hf-models` (mounted at `/models`, `HF_HOME`), so under `/data/docker`.
- The worker image runs with `HF_HUB_OFFLINE=1`: a run never downloads anything, and a missing model is an error that names the fix.
- Every deploy runs `python -m notinspec.nli fetch` once before `up`. It downloads the pinned revision the first time and after a revision bump, and is an offline no-op otherwise.

```sh
sudo docker compose -f deploy/docker-compose.yml --env-file /opt/notinspec/.env run --rm --no-deps   -e HF_HUB_OFFLINE=0 worker python -m notinspec.nli fetch     # by hand, e.g. after deleting the volume
sudo docker compose -f deploy/docker-compose.yml --env-file /opt/notinspec/.env run --rm --no-deps   worker python -m notinspec.nli bench --pairs 64            # speed on the VM (pairs/s = claims/s)
```

Old revisions stay on the volume after a bump. Free the space with `sudo docker volume rm notinspec_hf-models` (the next deploy fetches again).

## Mock service (Prism, SPEC §12)

`mock` runs Prism on uploaded specs, which are untrusted. It sits only on the `sandbox` network (`internal: true`, no internet) and has no secrets. It reads the `specs` volume read-only, and the worker writes to it. The worker picks the spec with `POST http://mock:4011/serve` ([deploy/mock/control.js](../deploy/mock/control.js)).

```sh
sudo docker exec notinspec-mock-1 wget -qO- http://127.0.0.1:4011/health   # {"serving": …}
sudo docker logs notinspec-mock-1   # Prism's output, also why a spec failed to load
```

## Database (SPEC §10)

Postgres holds everything (queue, results, raw LLM calls). Two roles:

- `notinspec`: the owner (`POSTGRES_PASSWORD`). Only `migrate` and `backup` connect as it.
- `notinspec_app` (`NOTINSPEC_APP_PASSWORD`): what `api` and `worker` connect as. It reads and inserts everywhere, updates and deletes only mutable tables, and cannot change the schema or UPDATE/DELETE append-only tables such as `llm_call` (privileges from [grants.py](../core/src/notinspec/db/grants.py), plus a trigger from migration 0001).

**Every deploy** runs the one-shot `migrate` service before `up` (and `up` waits for it again before `api` and `worker`): it creates `notinspec_app` if it is missing and sets its password from `.env`, then runs `notinspec db upgrade` as the owner, which migrates to the newest revision and refreshes the role's privileges. With nothing to migrate it is a no-op. To rotate the app password, change `NOTINSPEC_APP_PASSWORD` in `/opt/notinspec/.env` and redeploy.

```sh
sudo docker logs notinspec-migrate-1     # expect "role notinspec_app is ready", "the database is at the latest migration", "privileges ... up to date"
sudo docker compose -f deploy/docker-compose.yml --env-file /opt/notinspec/.env run --rm --entrypoint notinspec migrate db current   # which revision (as the owner)
```

**When `migrate` fails**, the deploy stops before `up`: the previous `api` and `worker` keep running. Postgres runs DDL in a transaction, so a failed migration leaves the schema as it was. (A bare `docker compose up` behaves differently: it removes the old `api` and `worker` first and leaves them stopped when `migrate` fails, so on the VM run `migrate` on its own first, as the deploy does.) Read `sudo docker logs notinspec-migrate-1`, fix it in a PR, and merge. Before merging a PR with a migration, take a dump by hand (see *Backups*):

```sh
sudo docker exec notinspec-postgres-1 pg_dump -U notinspec -Fc -f /tmp/before-migration.dump notinspec
sudo docker cp notinspec-postgres-1:/tmp/before-migration.dump /data/backups/
```

## Demo runs (docs/plans/demo-cli-web.md)

The site's run list (`/api/demo/runs`) reads folders on the volume `demo-runs`: read-only in `api`, writable at `/runs` in `worker`. Shortcut: files, not Postgres, until the DB models are settled (SPEC §18).

**Make a run on the VM** (in the running worker, as `app`, which owns `/runs`):

```sh
TAG=$(sudo docker inspect -f '{{.Config.Image}}' notinspec-worker-1 | cut -d: -f2)   # deployed commit
sudo docker exec -e NOTINSPEC_COMMIT=$TAG notinspec-worker-1 \
  notinspec demo --config core/examples/sphinx/trio/notinspec.yaml --runs-dir /runs --no-claims
```

With claims (urllib3, reuses the answers of the FIIT extractors stored in run 009, so these pages need no LLM call; `FIIT_API_KEY` in `/opt/notinspec/.env` is needed only for chunks not in the store, e.g. after the pages or the prompt changed; NLI takes minutes on the CPU):

```sh
sudo docker exec -e NOTINSPEC_COMMIT=$TAG notinspec-worker-1 \
  notinspec demo --config core/examples/sphinx/urllib3/notinspec.yaml --runs-dir /runs \
  --source user-guide --source reference/urllib3.util --source v2-migration-guide \
  --claims-store experiments/nli/runs/009-fiit-urllib3-demo/claims-store.jsonl
```

**Copy runs made on a laptop** (the API needs only `run.json` in each folder):

```powershell
# on the laptop, from the repo root
ssh notinspec 'mkdir -p /tmp/demo-runs'
Get-ChildItem tmp/runs -Directory | ForEach-Object { ssh notinspec "mkdir -p /tmp/demo-runs/$($_.Name)"; scp "$($_.FullName)/run.json" "notinspec:/tmp/demo-runs/$($_.Name)/" }
```

```sh
# on the VM
sudo docker cp /tmp/demo-runs/. notinspec-worker-1:/runs/ && rm -rf /tmp/demo-runs
```

**Import the runs into the database** (once after the database went live, and after copying more runs; already imported run IDs are skipped):

```sh
sudo docker exec notinspec-worker-1 notinspec db import-runs /runs
```

**List or delete runs:** `sudo docker exec notinspec-worker-1 ls /runs`, `sudo docker exec -u root notinspec-worker-1 rm -rf /runs/<run id>`. `-u root` because `docker cp` writes as root. Every deploy runs `chown -R app /runs`, so copied runs belong to `app` again after the next one.

## Backups (SPEC §6)

The `backup` service (in [deploy/docker-compose.yml](../deploy/docker-compose.yml)) runs `pg_dump` on start and every 24 h after that. It writes to `/data/backups/notinspec-<UTC time>.dump` and deletes dumps older than 14 days.

**Check it works:**

```sh
ls -lh /data/backups
sudo docker logs notinspec-backup-1     # expect "backup ok: ..."
```

**Off-machine copy (manual for now).** The dumps are on the same VM as the database. If the VM is lost, they are lost too. Until an automatic off-site target is chosen, pull the newest dump to your PC regularly, **at least weekly once real runs start**:

```powershell
$f = ssh notinspec 'ls -t /data/backups/*.dump | head -1'
scp "notinspec:$f" .
```

**Restore** (replaces the current database contents):

```sh
sudo docker cp /data/backups/<file>.dump notinspec-postgres-1:/tmp/restore.dump
sudo docker exec notinspec-postgres-1 pg_restore -U notinspec -d notinspec --clean --if-exists /tmp/restore.dump
```

Test a restore once before real data exists. A backup that was never restored is a guess.

## Giving a teammate SSH access

Ask for their **public** key (`~/.ssh/id_ed25519.pub` or similar), then on the VM:

```sh
echo 'ssh-ed25519 AAAA... name@team' >> ~/.ssh/authorized_keys
```

(OpenStack's *Import Public Key* rejects ed25519 keys. That only matters for the OpenStack dashboard; `authorized_keys` accepts them fine.)

## Gotchas we already hit

- **`cd /home/deploy/...` says Permission denied** as `ubuntu`. Home folders are private on Ubuntu 24.04. Use `sudo bash -c 'cd /home/deploy/actions-runner && ...'`.
- **sudo asks for a password**: you are logged in as `deploy` (which has none). `exit` back to `ubuntu`.
- **Deploy queued forever**: the runner is offline. Check its service (above). GitHub cancels queued jobs after 24 h, so re-run *Deploy* afterwards.
- **Never publish Postgres's port** in Compose. 5432 is open on the FIIT firewall, so publishing it exposes the database to the network.
- **Never run `mkfs` on `/dev/vdb` again.** It holds all data.

## Rebuilding the VM from scratch

Only if the instance is lost. Then restore the database from your off-machine dump.

1. OpenStack: launch `notinspec` from image `noble-server-cloudimg-amd64`, flavor `fiit.fiit-tp2026-team19`, boot volume ~40 GB (*Delete on instance delete: No*), security group `default` (already allows 22/80/443), your key pair. Create and attach an empty ~60 GB volume.
2. Data disk + Docker:
   ```sh
   sudo mkfs.ext4 -L notinspec-data /dev/vdb     # NEW empty disk only
   sudo mkdir -p /data && echo 'LABEL=notinspec-data /data ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab
   sudo systemctl daemon-reload && sudo mount /data
   sudo mkdir -p /etc/docker && echo '{"data-root": "/data/docker", "log-driver": "local"}' | sudo tee /etc/docker/daemon.json
   sudo apt-get update && sudo apt-get install -y docker.io docker-compose-v2
   ```
3. Deploy user + secrets:
   ```sh
   sudo useradd -m -s /bin/bash -G docker deploy
   sudo mkdir -p /opt/notinspec
   sudo tee /opt/notinspec/.env > /dev/null <<EOF
   POSTGRES_PASSWORD=$(openssl rand -hex 24)
   NOTINSPEC_APP_PASSWORD=$(openssl rand -hex 24)
   IMAGE_OWNER=19bros
   WEB_PORT=80
   HTTPS_PORT=443
   SITE_ADDRESS=147-175-151-17.sslip.io
   FIIT_API_KEY=
   GROQ_API_KEY=
   SLACK_WEBHOOK_URL=
   INGEST_TOKEN=$(openssl rand -hex 24)
   EOF
   sudo chown -R deploy:deploy /opt/notinspec && sudo chmod 600 /opt/notinspec/.env
   ```
   When restoring a dump, the new password is fine: `pg_restore` doesn't care.
4. Runner: remove the old offline runner in GitHub (Settings → Actions → Runners), then *New self-hosted runner* → Linux x64. As `deploy` (`sudo -iu deploy`), run the page's download commands and
   `./config.sh --url https://github.com/19BROS/not-in-spec --token <TOKEN> --labels notinspec-deploy --name notinspec-vm --unattended`.
   Then as `ubuntu`:
   `sudo bash -c 'cd /home/deploy/actions-runner && ./svc.sh install deploy && ./svc.sh start'`
5. GitHub → Actions → *Deploy* → re-run the latest successful run.
