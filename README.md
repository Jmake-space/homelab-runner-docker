# homelab-runner-docker

Self-hosted GitHub Actions runner (Docker) for the homelab.

## Setup
1. Copy the env file and set a fresh registration token:

```bash
cp .env.example .env
```

Get a token:

```bash
gh api -X POST /orgs/jmake-space/actions/runners/registration-token -q .token
```

2. Start the runner:

```bash
docker compose up -d
```

## Notes
- Compose selects a derived runner image whose Dockerfile installs Python 3 and
  OS `tzdata`. This supplies IANA timezone data for Python `ZoneInfo`, including
  `America/New_York`, without changing the runner's default timezone or user.
- Validate source and timezone behavior with
  `python3 -m unittest discover -s tests -v`. The image build also checks
  `ZoneInfo("America/New_York")`. Runtime dependency repairs survive process
  restarts but not container replacement; the derived image is the durable fix.
- Publish this change from the approved Mac via a PR to `main`; build/deploy
  through GitHub Actions after merge. Do not rebuild or replace a live runner
  during dependency-only incident recovery.
- Runner data is stored in `/home/jaideepbir/actions-runner-docker` on the host.
- Labels default to `pi5,docker` (override via `.env`).
- The runner is registered at the org level; add new public repos to the runner group if needed.
- For Docker builds, mount `/var/run/docker.sock` or switch to a Docker-in-Docker runner image.

## Add a repo to the runner group
```bash
./scripts/add-repo-to-runner-group.sh jmake-space/your-repo
```
