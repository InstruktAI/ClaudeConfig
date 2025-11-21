#!/usr/bin/env sh
set -e

. .venv/bin/activate

# Separate skills files from regular files
skills_files=""
regular_files=""

if [ $# -gt 0 ]; then
  # Files passed from pre-commit
  for file in "$@"; do
    case "$file" in
      skills/*)
        skills_files="$skills_files $file"
        ;;
      *)
        regular_files="$regular_files $file"
        ;;
    esac
  done
else
  # Default: lint hooks, scripts, utils (regular) and skills separately
  regular_files="hooks scripts utils"
  skills_files="skills"
fi

echo "Running lint checks"

# Lint regular code with strict rules
if [ -n "$regular_files" ]; then
  echo "Running pylint"
  pylint $regular_files
fi

# Lint skills with relaxed rules for example/template code
# Focus only on real errors (F, E) and critical warnings
# Disable style issues since skills are examples/templates
if [ -n "$skills_files" ]; then
  echo "Running pylint"
  pylint --rcfile=/dev/null --disable=all --enable=F,E --disable=import-error $skills_files
fi

# TODO: Fix 20 mypy type annotation errors and re-enable
# echo "Running mypy"
# mypy $files
