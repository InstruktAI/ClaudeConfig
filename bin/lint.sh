#!/usr/bin/env sh
set -e

. .venv/bin/activate

# If filenames are passed (from pre-commit), lint only those files
# Otherwise lint hooks, scripts, utils
if [ $# -gt 0 ]; then
  files="$@"
else
  files="hooks scripts utils"
fi

echo "Running lint checks"

echo "Running pylint"
pylint $files

# TODO: Fix 20 mypy type annotation errors and re-enable
# echo "Running mypy"
# mypy $files
