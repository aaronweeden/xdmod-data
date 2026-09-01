# Downgrade the dependencies of xdmod-data to the lowest versions that are
# documented as supported by xdmod-data.
# See docs/developing.md for local testing instructions.

import subprocess

# Import the script for getting config data.
dir_ = Path(__file__).resolve().parent
if str(dir_) not in sys.path:
    sys.path.insert(0, str(dir_))
import get_config

downgraded_dependencies = [
    x.replace(" >= ", "==") for x in get_config.get_dependencies()
]

subprocess.run(
    "python3 -m pip install --force-reinstall".split() + downgraded_dependencies,
    check=True,
)
