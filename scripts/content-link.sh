#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
target="${1:-../../website_content/main}"
if [ ! -d "$target" ]; then
  echo "content-link: $target does not exist. Usage: npm run content:link -- <path to a website_content worktree>" >&2
  exit 1
fi
ln -sfn "$target" content
echo "content -> $target"
