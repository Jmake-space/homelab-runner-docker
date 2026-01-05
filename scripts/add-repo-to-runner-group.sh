#!/usr/bin/env bash
set -euo pipefail

org="${ORG:-jmake-space}"
group="${GROUP:-public-repos}"
repo="${1:-}"

if [[ -z "$repo" ]]; then
  echo "Usage: $0 <owner/repo>"
  exit 1
fi

if [[ "$repo" =~ ^https?://github.com/([^/]+/[^/]+)(/)?$ ]]; then
  repo="${BASH_REMATCH[1]}"
fi

if [[ "$repo" != */* ]]; then
  echo "Repo must be in owner/repo format or a GitHub URL."
  exit 1
fi

repo_id="$(gh api "/repos/${repo}" -q '.id')"
group_id="$(gh api "/orgs/${org}/actions/runner-groups" -q ".runner_groups[] | select(.name==\"${group}\") | .id")"

if [[ -z "$group_id" ]]; then
  echo "Runner group not found: ${group}"
  exit 1
fi

gh api -X PUT "/orgs/${org}/actions/runner-groups/${group_id}/repositories/${repo_id}" >/dev/null
echo "Added ${repo} to runner group ${group} (org: ${org})."
