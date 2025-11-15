#!/usr/bin/env sh
set -e

. .venv/bin/activate

# If filenames are passed (from pre-commit), format only those files
# Otherwise format hooks, scripts, utils
if [ $# -gt 0 ]; then
  files="$@"
else
  files="hooks scripts utils"
fi

echo "Running isort"
python -m isort $files

echo "Running black"
black $files

# Auto-add formatted files back to staging area (pre-commit hook)
if [ $# -gt 0 ]; then
  git add $files
fi
