#!/usr/bin/env bash
#
# Create docs in docs/
#

lazydocs \
    --output-path="./docs/docstrings" \
    --overview-file="README.md" \
    --src-base-url="https://github.com/andgineer/ellipsize/blob/master/" \
    src/ellipsize

mkdocs build
