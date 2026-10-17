# NOT-IN-SPEC — Deployment runbook

How production runs, and what to do when something breaks. For the design behind it, see [SPEC.md §8](SPEC.md#8-devops).

## At a glance

| | |
|---|---|
| Site | http://147.175.151.17 (API: `/api/health`) — **faculty VPN required** |
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

1. `CI` runs on the push to `main`: lint, tests, Compose smoke test, then pushes `api`, `worker`, `web` images to GHCR tagged with the commit SHA.
2. When CI succeeds, `Deploy` runs on the **self-hosted runner on the VM** (label `notinspec-deploy`, environment `production`).
3. It checks out that commit, pulls the images for that SHA and runs `docker compose up -d` with `/opt/notinspec/.env`.

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
sudo docker logs -f --tail 100 notinspec-api-1    # logs of one service (api, worker, web, postgres, backup)
sudo systemctl status 'actions.runner.*'          # is the runner alive?
sudo systemctl restart 'actions.runner.*'         # restart it
df -h / /data                                     # disk space
```

## Rollback / redeploy

- **Redeploy the current version:** GitHub → Actions → *Deploy* → latest run → *Re-run jobs*.
- **Roll back:** GitHub → Actions → *Deploy* → open an older **successful** run → *Re-run jobs*. It redeploys that run's commit and images.
- Better long-term: revert the bad PR on `main`. That deploys automatically.

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
   IMAGE_OWNER=19bros
   WEB_PORT=80
   OPENROUTER_API_KEY=
   SLACK_WEBHOOK_URL=
   EOF
   sudo chown -R deploy:deploy /opt/notinspec && sudo chmod 600 /opt/notinspec/.env
   ```
   When restoring a dump, the new password is fine: `pg_restore` doesn't care.
4. Runner: remove the old offline runner in GitHub (Settings → Actions → Runners), then *New self-hosted runner* → Linux x64. As `deploy` (`sudo -iu deploy`), run the page's download commands and
   `./config.sh --url https://github.com/19BROS/not-in-spec --token <TOKEN> --labels notinspec-deploy --name notinspec-vm --unattended`.
   Then as `ubuntu`:
   `sudo bash -c 'cd /home/deploy/actions-runner && ./svc.sh install deploy && ./svc.sh start'`
5. GitHub → Actions → *Deploy* → re-run the latest successful run.
