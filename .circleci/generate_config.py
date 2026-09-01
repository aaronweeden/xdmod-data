# Generate CircleCI config. This is done so the minimum and maximum Python
# versions do not have to be redundantly declared in multiple files.

from pathlib import Path
import sys

# Import the script for getting config data.
dir_ = Path(__file__).resolve().parent / ".." / "tests" / "scripts"
if str(dir_) not in sys.path:
    sys.path.insert(0, str(dir_))
import get_config

# Generate the config.
output_config = f"""
version: 2.1

jobs:
  lint:
    docker:
      - image: cimg/python:{get_config.get_max_python_version()}
    resource_class: small
    steps:
      - checkout
      - run:
          name: Install Flake8
          command: python3 -m pip install --upgrade flake8 flake8-commas flake8-quotes
      - run:
          name: Run Flake8
          command: python3 -m flake8 . --max-complexity=10 --max-line-length=160 --show-source --exclude __init__.py
"""
for python_version in [
    get_config.get_min_python_version(),
    get_config.get_max_python_version(),
]:
    output_config += f"""
  test_python_{python_version}:
    docker:
      - image: cimg/python:{python_version}
        name: xdmod-data-python-{python_version}
    """
    for image in get_config.get_xdmod_images():
        output_config += f"""
      - image: tools-ext-01.ccr.xdmod.org/xdmod:{image}
        name: {image}
    """
    output_config += """
    resource_class: small
    steps:
      - checkout
      - run: python3 ./tests/scripts/setup.py
    """
    if python_version == get_config.get_min_python_version():
        output_config += """
      - run: python3 ./tests/scripts/downgrade_dependencies.py
        """
    output_config += f"""
      - run: python3 ./tests/scripts/run_tests.py
    """
output_config += """
workflows:
  lint:
    jobs:
      - lint
  run_tests:
    jobs:
"""
for python_version in [
    get_config.get_min_python_version(),
    get_config.get_max_python_version(),
]:
    output_config += f"""
      - test_python_{python_version}
    """

# Output the config.
print(output_config)
