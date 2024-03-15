# Copyright 2018 Databricks, Inc.
import re

VERSION = "2.64.0"


def is_release_version():
    return bool(re.match(r"^\d+\.\d+\.\d+$", VERSION))



