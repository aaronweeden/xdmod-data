# Downgrade the dependencies of xdmod-data to the lowest versions that are
# documented as supported by xdmod-data.

from pathlib import Path
import subprocess
import sys

# Import the script for getting config data.
parent_dir = Path(__file__).resolve().parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))
import get_config

downgraded_dependencies = [
    x.replace(" >= ", "==") for x in get_config.get_dependencies()
]

subprocess.run(
    "python3 -m pip install --force-reinstall".split() + downgraded_dependencies,
    check=True,
)
