#!/bin/bash
# Convert docs/notebooks/*.ipynb to markdown alongside (zensical does not render
# notebooks). Not executed -- uses the outputs saved in each notebook.
#
# CI runs this and fails if docs/notebooks/ changes, so run it and commit the
# result after editing a notebook. nbconvert is pinned so CI and local output
# match; bump it here (and re-run + commit) to upgrade.
#
# Lib READMEs are not handled here: libs/<lib>/README.md is the source of truth
# and docs/libs/<lib>/README.md includes it via a pymdownx.snippets `--8<--` line.

set -euo pipefail

uvx --from nbconvert==7.17.2 jupyter-nbconvert --to markdown docs/notebooks/*.ipynb

# nbconvert's indent filter is platform-dependent (it checks os.linesep, so on
# Windows output blocks keep a trailing "    " line). Normalize so Windows and
# Linux produce identical files: LF endings, whitespace-only lines emptied.
sed -i -e 's/\r$//' -e 's/^[[:space:]]*$//' docs/notebooks/*.md
