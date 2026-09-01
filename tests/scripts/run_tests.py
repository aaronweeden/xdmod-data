# Run Pytest tests.

import os
from pathlib import Path
import subprocess
import sys

# Import the script for getting config data.
parent_dir = Path(__file__).resolve().parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))
import get_config

if len(sys.argv) > 1:
    pytest_args = " ".join(sys.argv[1:])
else:
    pytest_args = "tests/pytest/"

# Run the tests against each XDMoD container.
for image in get_config.get_xdmod_images():
    container_name = get_config.get_container_name(image)
    if container_name is None:
        container_name = image
    print(f"Running tests for {container_name}", flush=True)
    os.environ["REQUESTS_CA_BUNDLE"] = f"{container_name}.crt"
    os.environ["XDMOD_CONTAINER"] = image.replace("xdmod-data-", "")
    os.environ["XDMOD_HOST"] = f"https://{container_name}"
    os.environ["TOKEN_PATH"] = f"{container_name}.token"
    subprocess.run(
        f"python3 -m coverage run --branch --append -m pytest -vvs -o log_cli=true {pytest_args}".split(),
        check=True,
    )

# Make sure all the code was covered by tests.
subprocess.run("python3 -m coverage report -m".split(), check=True)
