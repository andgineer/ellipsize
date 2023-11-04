#!/usr/bin/env bash
#
# Create docs in docs/
#

docstrings.sh

mkdocs build --config-file docs/mkdocs-en.yml
mkdocs build --dirty --config-file docs/mkdocs-ru.yml
