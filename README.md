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
- Runner data is stored in `/home/jaideepbir/actions-runner-docker` on the host.
- Labels default to `pi5,docker` (override via `.env`).
- The runner is registered at the org level; add new public repos to the runner group if needed.

## Add a repo to the runner group
```bash
./scripts/add-repo-to-runner-group.sh jmake-space/your-repo
```
