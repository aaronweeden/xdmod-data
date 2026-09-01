#!/bin/bash

set -euo pipefail

cd $(dirname "${BASH_SOURCE[0]}")/../..
python3 -m pip install -e .[report] black coverage flake8 pytest python-dotenv pyyaml tenacity tomli
