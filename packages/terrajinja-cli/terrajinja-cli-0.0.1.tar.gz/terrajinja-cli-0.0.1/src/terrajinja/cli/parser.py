import logging
import os

from .parse_args import ParseArgs
from .parse_jinja import ParseJinja

logger = logging.getLogger(__name__)


class ParseConfig:
    def __init__(self):
        self.jinja = ParseJinja()
        self.parse_args = ParseArgs(self.jinja)

    def get_config(self) -> dict:
        """parses all config files

        Returns:
            dict: merge of all configs

        """
        # get initial arguments and read parameters
        args, _ = self.parse_args.parse_known_args()
        parameter_path = os.path.join(args.config_directory, 'parameters')
        deployments_path = os.path.join(args.config_directory, 'deployments')
        templates_path = os.path.join(args.config_directory, 'templates')

        # read all parameter files
        parameters = self.jinja.parse_directory(path=parameter_path)

        # read the deployment arg
        deployment = self.parse_args.get_deployment(path=deployments_path, parameters=parameters)

        # parse deployment input requirements and enhance parameters with the result
        parameters = self.parse_args.parse_deployment_input(deployment=deployment, parameters=parameters)

        # re-read the deployment file so that its jinja parsed too for the templates etc
        parameters = self.jinja.parse_file(filename=os.path.join(deployments_path, f"{parameters['deployment']}.yaml"),
                                           parameters=parameters)

        # finally parse the templates
        parameters = self.parse_templates(templates_path, parameters)
        return parameters

    def parse_templates(self, path: str, parameters: dict) -> dict:
        """parse all template files using the parameters provided

        Args:
            path: directory to the parameter files
            parameters: dict to use as input for the parameter files

        Returns:
            dict: formatted templates merged in a single dict

        """
        templates = parameters.get("templates")
        if templates:
            for template_filename, version in templates.items():
                parameters = self.jinja.parse_file(
                    filename=os.path.join(path, f"{template_filename}_v{version}.yaml",
                                          ),
                    parameters=parameters,
                )

        return parameters
