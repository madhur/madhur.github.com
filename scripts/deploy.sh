#!/usr/bin/env bash
# Build the Hugo site and push the built output to `master`, which GitHub
# Pages serves directly (branch-based Pages, not GitHub Actions).
#
# Mirrors the old Jekyll pipeline: `_config.yml` used to build to a sibling
# `../site/` checkout of `master`, and the Gulpfile's git tasks committed and
# pushed it. This script does the same thing for Hugo: builds straight into
# a sibling git worktree of `master`, commits, and pushes.
#
# Usage:
#   scripts/deploy.sh            # build, commit, and push
#   scripts/deploy.sh --dry-run  # build and stage the commit, but don't push
set -euo pipefail

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
SITE_WORKTREE="$REPO_ROOT/../site"

cd "$REPO_ROOT"

CURRENT_BRANCH="$(git branch --show-current)"
if [[ "$CURRENT_BRANCH" != "source" ]]; then
  echo "warning: deploying from branch '$CURRENT_BRANCH', not 'source' — make sure that's intended." >&2
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "error: uncommitted changes on '$CURRENT_BRANCH' — commit or stash before deploying." >&2
  exit 1
fi

# Set up (or refresh) the sibling master worktree that Hugo builds into.
if [[ ! -d "$SITE_WORKTREE" ]]; then
  echo "==> Creating $SITE_WORKTREE as a worktree of master"
  git worktree add "$SITE_WORKTREE" master
fi

echo "==> Syncing $SITE_WORKTREE to latest origin/master"
git -C "$SITE_WORKTREE" fetch origin master
git -C "$SITE_WORKTREE" checkout master
git -C "$SITE_WORKTREE" reset --hard origin/master
git -C "$SITE_WORKTREE" clean -fdx

echo "==> Building site (hugo --minify --environment production)"
hugo --minify --environment production --destination "$SITE_WORKTREE" --cleanDestinationDir

cd "$SITE_WORKTREE"

if [[ -z "$(git status --porcelain)" ]]; then
  echo "==> Nothing changed, site is already up to date."
  exit 0
fi

git add -A
COMMIT_MSG="Repository updated on $(date -u +'%Y-%m-%dT%H:%M:%S.%3NZ')"
git commit -m "$COMMIT_MSG"

if $DRY_RUN; then
  echo "==> --dry-run: committed locally in $SITE_WORKTREE, NOT pushed. Run without --dry-run to push."
  exit 0
fi

echo "==> Pushing to origin/master"
git push origin master
echo "==> Done."
