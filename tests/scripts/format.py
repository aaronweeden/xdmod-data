from pathlib import Path
import subprocess
import sys

# Import the script for getting config data.
parent_dir = Path(__file__).resolve().parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))
import get_config

subprocess.run(
    f"python3 -m black --target-version=py{str(get_config.get_max_python_version()).replace('.', '')} {parent_dir / '..' / '..'}".split(),
    check=True,
)
