import argparse
import logging
import os

logger = logging.getLogger(__name__)


class KeyNotInPath(Exception):
    """key does not exist in path"""


def dotdict(dotpath: str, dictionary: dict) -> any:
    """Get the path from a dict based on a dotted path notation

    Args:
        dotpath (str): path of the variable to fetch
        dictionary (dict): dict to fetch the variable from

    Raises:
        ValueError: _description_

    Returns:
        any: result of the item in dict
    """
    path = dotpath.split(".")
    if not dictionary.get(path[0]):
        raise KeyNotInPath(f"unable to parse dotted string '{dotpath}' does not exist in the parameters")
    if len(path) > 1:
        return dotdict(".".join(path[1:]), dictionary[path[0]])
    return dictionary[path[0]]


def parse_variables(input_string: str, parameters: dict) -> str:
    """replace variables in a string based on a dictionary
        replaces strings that start with a '$' with the value of the key with this name

    Args:
        input_string (str): string that contains variables
        parameters (dict): dictionary of variables and values to apply

    Returns:
        str: formatted string
    """
    temp = []
    for word in input_string.split("."):
        if word[0] == "$":
            word = parameters.get(word[1:], word)
        temp.append(word)
    res = ".".join(temp)
    return res


class ParseArgs:
    """Parse commandline arguments, and generate choices based on existing files"""

    def __init__(self, jinja: any, parameters: dict = None):
        if parameters is None:
            parameters = {}
        self.jinja = jinja
        self.parameters = parameters
        self.parser = argparse.ArgumentParser()
        # default parameters which are always available
        self.parser.add_argument(
            "-C",
            "--config-directory",
            # default=os.path.join(os.path.dirname(os.path.realpath(__file__)), "config"),
            default=os.path.join(os.getcwd(), "config"),
            help="path to the config directory",
        )
        self.parser.add_argument(
            "-a",
            "--action",
            required=False,
            choices=["plan", "apply", "destroy"],
            help="Action to perform on the deployment",
        )
        self.parser.add_argument(
            "-l",
            "--loglevel",
            choices=["debug", "info", "warning", "error", "critical"],
            help="Set the logging level (default: %(default)s)",
            default="INFO",
        )

    @staticmethod
    def get_file_base_names_from_path(path: str) -> list[str]:
        """get available deployments"""
        return [x.split(".")[0] for x in os.listdir(path)]

    def get_deployment(self, path: str, parameters: dict) -> dict:
        """parse argument of deployment, and get additional arguments from the deployment yaml"""
        self.parser.add_argument(
            "-d",
            "--deployment",
            required=True,
            choices=self.get_file_base_names_from_path(path),
            help="Name of the deployment",
        )
        args, _unknown = self.parser.parse_known_args()
        return self.jinja.parse_file(os.path.join(path, f"{args.deployment}.yaml"))

    def parse_deployment_input(self, deployment, parameters) -> dict:
        required_input = deployment.get("required_input")
        if not required_input:
            return parameters

        for arg, config in required_input.items():
            choices = config.get("choices")
            if choices and not isinstance(choices, list):
                parameter = dotdict(parse_variables(choices, parameters), parameters)
                if isinstance(parameter, dict):
                    config["choices"] = [x for x in parameters.get(choices).keys()]
                if isinstance(parameter, str):
                    config["choices"] = [parameters]

            default = config.get("default")
            if default:
                if "." in default:
                    config["default"] = dotdict(parse_variables(default, parameters), parameters)

            self.parser.add_argument(f"-{arg[0]}", f"--{arg}", **config)

            # after each arg, parse it, so it can be used as input in the next if needed, merge it in parameters
            args, _unknown = self.parser.parse_known_args()
            parameters = self.jinja.merge(vars(args), parameters)
        return parameters

    def parse_args(self) -> argparse:
        """return all current parsable arguments"""
        return self.parser.parse_args()

    def parse_known_args(self) -> argparse:
        """return all current parsable arguments"""
        return self.parser.parse_known_args()
