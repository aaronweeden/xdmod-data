# Run Pytest tests.

import get_config
import os
from pathlib import Path
import subprocess
import sys

if len(sys.argv) > 1:
    pytest_args = " ".join(sys.argv[1:])
else:
    pytest_args = "tests/pytest/"

# Run the tests against each XDMoD container.
for image in get_config.get_xdmod_images():
    container_name = get_config.get_container_name(image, default=image)
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
