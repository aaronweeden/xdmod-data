#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR=${SCRIPT_DIR}/../..

echo 'Formatting with Black...'
python3 ${PROJECT_DIR}/tests/scripts/format.py --check

echo 'Linting with Flake8...'
python3 -m flake8 --select C90,F401,F841 --max-complexity 10 --exclude __init__.py ${PROJECT_DIR}
echo 'Linting successful'
