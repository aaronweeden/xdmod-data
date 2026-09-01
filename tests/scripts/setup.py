# Install xdmod-data in editable mode and get API tokens for each of the XDMoD
# containers.
# See docs/developing.md for local testing instructions.

from pathlib import Path
import subprocess
import sys
import warnings

subprocess.run(
    "python3 -m pip install -e .[report] pytest pytest-cov python-dotenv pyyaml".split(),
    check=True,
)

import requests
from urllib3.exceptions import InsecureRequestWarning

# Import the script for getting config data.
dir_ = Path(__file__).resolve().parent
if str(dir_) not in sys.path:
    sys.path.insert(0, str(dir_))
import get_config

for image in get_config.get_xdmod_images():
    container_name = get_config.get_container_name(image)
    if container_name is None:
        container_name = image

    # Get the certificate file from the XDMoD container.
    print(f"Getting certificate file from {container_name}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InsecureRequestWarning)
        response = requests.get(f"https://{container_name}/localhost.crt", verify=False)
    response.raise_for_status()
    with open(f"{container_name}.crt", "wb") as cert_file:
        cert_file.write(response.content)

    # Open a requests session.
    session = requests.Session()
    session.verify = f"{container_name}.crt"

    # Get an auth token.
    print(f"Getting auth token from {container_name}")
    response = session.post(
        f"https://{container_name}/rest/auth/login",
        data={"username": "normaluser", "password": "normaluser"},
    )
    response.raise_for_status()
    auth_token = response.json()["results"]["token"]

    # Delete any API token that already exists.
    print(f"Deleting API token on {container_name}")
    response = session.delete(
        f"https://{container_name}/rest/users/current/api/token?token={auth_token}"
    )
    if response.status_code not in [200, 404]:
        response.raise_for_status()

    # Create an API token.
    print(f"Creating API token on {container_name}")
    response = session.post(
        f"https://{container_name}/rest/users/current/api/token?token={auth_token}"
    )
    response.raise_for_status()

    # Save the API token to a file.
    print(f"Saving API token to {container_name}.token")
    with open(f"{container_name}.token", "w") as token_file:
        token_file.write(f"XDMOD_API_TOKEN={response.json()['data']['token']}")
