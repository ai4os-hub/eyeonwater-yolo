"""Module to define CONSTANTS used across the DEEPaaS Interface.

This module is used to define CONSTANTS used across the API interface.
Do not misuse this module to define variables that are not CONSTANTS.

By convention, the CONSTANTS defined in this module are in UPPER_CASE.
"""

import logging
import os
from importlib import metadata

from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parents[1]

# Get AI model metadata from pyproject.toml
API_NAME = "eyeonwater-yolo"
PACKAGE_METADATA = metadata.metadata(API_NAME)  # .json

# Get ai4-metadata.yaml metadata (default location: BASE_DIR)
AI4_METADATA_DIR = os.getenv(f"{API_NAME.capitalize()}_AI4_METADATA_DIR",
                             BASE_DIR)

# Open ai4-metadata.yml
_file = f"{AI4_METADATA_DIR}/ai4-metadata.yml"
with open(_file, "r", encoding="utf-8") as stream:
    AI4_METADATA = yaml.safe_load(stream)

# Project metadata
# License is deprecated since v2.4 of metadata:
# in favour of License-Expression.
PROJECT_METADATA = {
  "name": PACKAGE_METADATA["Name"],
  "description": AI4_METADATA["description"],
  "license": PACKAGE_METADATA["License-Expression"],
  "version":  PACKAGE_METADATA["Version"],
  "url":  PACKAGE_METADATA["Project-URL"],
}

# Fix metadata for authors and emails from pyproject parsing
_EMAILS_LIST = PACKAGE_METADATA["Author-email"].split(", ")
_EMAILS = dict(map(lambda s: s[:-1].split(" <"), _EMAILS_LIST))
PROJECT_METADATA["author-email"] = _EMAILS
_AUTHOR = ", ".join(PROJECT_METADATA["author-email"].keys())
PROJECT_METADATA["author"] = _AUTHOR

# logging level across API modules can be setup via API_LOG_LEVEL,
# options: DEBUG, INFO(default), WARNING, ERROR, CRITICAL
ENV_LOG_LEVEL = os.getenv("API_LOG_LEVEL", default="INFO")
LOG_LEVEL = getattr(logging, ENV_LOG_LEVEL.upper())
