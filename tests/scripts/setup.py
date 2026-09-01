# Install xdmod-data in editable mode and get API tokens for each of the XDMoD
# containers.

from pathlib import Path
import subprocess
import sys
import warnings

parent_dir = Path(__file__).resolve().parent

subprocess.run(
    f"{parent_dir}/install_dependencies.sh".split(),
    check=True,
)

import requests
from requests.exceptions import RequestException
from urllib3.exceptions import InsecureRequestWarning
import tenacity

# Import the script for getting config data.
parent_dir = Path(__file__).resolve().parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))
import get_config


# Define a function for trying to get the self-signed certificate file from the
# XDMoD web server every second for up to one minute (this is so the web server
# has time to start up before making requests to it).
@tenacity.retry(
    retry=tenacity.retry_if_exception_type(RequestException),
    stop=tenacity.stop_after_attempt(60),
    wait=tenacity.wait_fixed(1),
    reraise=True,
)
def get_certificate_file(container_name):
    print(f"Getting certificate file from {container_name}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InsecureRequestWarning)
        response = requests.get(f"https://{container_name}/localhost.crt", verify=False)
    response.raise_for_status()
    with open(f"{container_name}.crt", "wb") as cert_file:
        cert_file.write(response.content)


for image in get_config.get_xdmod_images():
    container_name = get_config.get_container_name(image)
    if container_name is None:
        container_name = image

    # Open a requests session that retries a few times to give the XDMoD web
    # server time to start up.
    session = requests.Session()

    # Get the certificate file from the XDMoD container.
    get_certificate_file(container_name)
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
