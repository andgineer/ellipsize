#!/usr/bin/env bash
#
# Create docs in docs/
#

lazydocs \
    --output-path="./docs/en/api-reference" \
    --overview-file="index.md" \
    --src-base-url="https://github.com/andgineer/ellipsize/blob/master/" \
    src/ellipsize

cp -r ./docs/en/api-reference ./docs/ru/api-reference

mkdocs build --config-file docs/mkdocs-en.yml
mkdocs build --dirty --config-file docs/mkdocs-ru.yml
