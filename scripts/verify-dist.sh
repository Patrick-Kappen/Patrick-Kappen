#!/bin/sh
set -eu
dist="${1:-dist}"
fail=0

for page in index.html blog/index.html work/index.html setup/index.html about/index.html contact/index.html 404.html rss.xml sitemap-index.xml now.json _headers; do
  if [ ! -s "$dist/$page" ]; then
    echo "missing or empty: $dist/$page" >&2
    fail=1
  fi
done

if [ -n "$(find "$dist" -name '*.html' -print -quit)" ]; then
  if grep -rnE --include='*.html' '<style|[[:space:]]style=' "$dist"; then
    echo "inline style found" >&2
    fail=1
  fi
  if grep -rnE --include='*.html' '<script([^>]*)>' "$dist" | grep -vE '<script[^>]*[[:space:]]src=' ; then
    echo "inline script found" >&2
    fail=1
  fi
fi

exit "$fail"
