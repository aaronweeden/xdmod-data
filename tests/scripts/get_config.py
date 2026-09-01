# Define functions to get configuration data. This allows multiple scripts to
# use these data without having to define them in multiple places.

from pathlib import Path
import tomli
import yaml

with open(
    Path(__file__).resolve().parent / ".." / ".." / "pyproject.toml", "rb"
) as pyproject_file:
    pyproject_config = tomli.load(pyproject_file)

with open(
    Path(__file__).resolve().parent / ".." / "config.yml", "r"
) as tests_config_file:
    tests_config = yaml.safe_load(tests_config_file)


def get_min_python_version():
    return pyproject_config["project"]["requires-python"].replace(">= ", "")


def get_max_python_version():
    return tests_config["max_python_version"]


def get_dependencies():
    return pyproject_config["project"]["dependencies"]


def get_xdmod_images():
    return tests_config["xdmod_images"]


def get_container_name(image, default):
    if "container_names" not in tests_config:
        return default
    if image not in tests_config["container_names"]:
        return default
    if tests_config["container_names"][image] is None:
        return "null"
    return tests_config["container_names"][image]


def get_network_name(default):
    if "network_name" not in tests_config or tests_config["network_name"] is None:
        return default
    return tests_config["network_name"]
