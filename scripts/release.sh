#!/usr/bin/env bash
# Cut a release: one tag, pointing at one commit, for ever.
#
#   scripts/release.sh v4.17.0
#
# There are no floating tags. A tag force-pushed onto a later commit means two
# builds of the same workflow, at the same ref, against different code — that
# is not a version, it is a moving target wearing one. Consumers pin the exact
# release and upgrade when they choose to.
#
# `v4` is a branch, not a tag. It used to be a tag that this repository moved
# onto each new release, which is the thing being fixed: a ref that moves should
# look like one. As a branch it is the major line's development head, and the
# manifests reach for each other at @v4 — so dAppCore/build@v4 gets the whole
# tree as it stands, sub-actions included, and that is what dAppCore's own
# repositories consume. A mistake lands on us before it reaches anyone pinned to
# a release.
#
# A release cannot ship those @v4 references: the root action of vX would run
# whatever the sub-actions happen to be that afternoon. So the tag is built on a
# detached commit with every internal reference rewritten to the version being
# cut. The branch keeps its @v4 references and is never rewritten.

set -euo pipefail

cd "$(dirname "$0")/.."

VERSION="${1:-}"
if ! printf '%s' "$VERSION" | grep -qE '^v[0-9]+\.[0-9]+\.[0-9]+$'; then
  echo "usage: $0 vMAJOR.MINOR.PATCH" >&2
  exit 1
fi

git fetch --tags --quiet origin

if git rev-parse -q --verify "refs/tags/$VERSION" >/dev/null; then
  echo "error: $VERSION already exists — versions go up, they never move" >&2
  exit 1
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [ "$BRANCH" != "main" ]; then
  echo "error: releases are cut from main, not $BRANCH" >&2
  exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
  echo "error: working tree is dirty — commit or stash first" >&2
  exit 1
fi

MAIN="$(git rev-parse HEAD)"
# Detached, so nothing below can rewrite main. Restored on any exit.
cleanup() { git checkout -q "$BRANCH" 2>/dev/null || true; }
trap cleanup EXIT
git checkout -q --detach "$MAIN"

for f in $(grep -rl 'uses: dAppCore/build' action.yml actions | sort); do
  perl -pi -e "s{(uses: dAppCore/build[A-Za-z0-9/._-]*)\@[A-Za-z0-9._-]+}{\$1\@$VERSION}g" "$f"
done

# The contract check refuses a tree whose internal references disagree, so a
# rewrite that missed a file fails here rather than at some consumer's build.
python3 tests/action_contracts.py

git -c user.name="${GIT_AUTHOR_NAME:-$(git config user.name)}" \
    -c user.email="${GIT_AUTHOR_EMAIL:-$(git config user.email)}" \
    commit -qam "release: $VERSION

Internal action references pinned to this tag, so the root action and every
sub-action it reaches are one release. main keeps its @main references."

git tag "$VERSION"
git push origin "$VERSION"

echo
echo "released $VERSION at $(git rev-parse --short HEAD)"
echo "main is untouched at $(git rev-parse --short "$MAIN")"
echo "consumers pin:  uses: dAppCore/build@$VERSION"
echo "we dogfood:     uses: dAppCore/build@v4"
