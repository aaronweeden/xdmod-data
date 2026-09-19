# Install dependencies from pip.

from pathlib import Path
import subprocess

project_dir = Path(__file__).resolve().parent / ".." / ".."

subprocess.run(
    f"python3 -m pip install -e .[report] black coverage flake8 pytest python-dotenv pyyaml tenacity tomli".split(),
    check=True,
)
