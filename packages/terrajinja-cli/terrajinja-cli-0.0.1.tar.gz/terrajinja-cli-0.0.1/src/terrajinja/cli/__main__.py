#!/usr/bin/env python

import logging

import yaml

from . import ParseConfig
from terrajinja.deploy import TerraformDeployment

#if __name__ == "__main__":
def main():
    logger = logging

    parser = ParseConfig()
    parameters = parser.get_config()

    logger.basicConfig(
        format="%(asctime)s %(message)s",
        level=logging.getLevelName(parameters.get("loglevel").upper()),
    )

    logger.debug(yaml.safe_dump(parameters))

    terraform_config = parameters.get("terraform")
    exit(1)
    if terraform_config:
        app = TerraformDeployment(name=parameters["deployment"])
        app.compile(
            terraform_config.get("providers"), terraform_config.get("resources")
        )
        app.action(parameters["action"])
