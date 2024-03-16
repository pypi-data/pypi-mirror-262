import logging
import os
import sys
import shutil

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

        if args.command == "template":
            self.use_template(args)
            exit(0)

        if args.command == "init":
            self.init_dir(args)
            exit(0)

        parameter_path = os.path.join(args.config_directory, 'parameters')
        deployments_path = os.path.join(args.config_directory, 'deployments')
        templates_path = os.path.join(args.config_directory, 'templates')

        # read all parameter files
        parameters = self.jinja.parse_directory(path=parameter_path)
        # if parameters is empty, no parameters where provided in yaml, odd but sure, your new
        if not parameters:
            print(f'warn: no parameters were read from the parameter path {parameter_path}, this is unexpected')

        # read the deployment arg
        deployment = self.parse_args.get_deployment(path=deployments_path, parameters=parameters)

        # parse deployment input requirements and enhance parameters with the result
        parameters = self.parse_args.parse_deployment_input(deployment=deployment, parameters=parameters)
        if not parameters:
            print(f'error: no parameters were read from the provided deployment file, please provide a yaml file as input')
            exit(1)

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
    def init_dir(self, args: any):
        action = False
        for sub in ["deployments", "templates", "parameters"]:
            _path = os.path.join(args.config_directory, sub)
            if not os.path.exists(_path):
                print('creating directory', _path)
                os.mkdir(_path)
                action = True

        if not action:
            print('init already done, have a look at the template sub command to add a template (tjcli template -l)')
            exit(1)

        print('initial directories created, have a look at the template sub command to add a template (tjcli template -l)')

    def use_template(self, args: any):
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')

        if args.list:
            print('available templates:')
            for root, dirs, filenames in os.walk(template_dir):
                if len(dirs) == 1:
                    description = open(os.path.join(template_dir, dirs[0], 'description.txt')).read()
                    print(f'  {dirs[0]}: {description}')

        if args.add:
            print('requesting to add template {args.template}...')
            template_named_dir = os.path.join(template_dir, args.add)
            if not os.path.exists(template_named_dir):
                print(f'error: non-existing template: {args.add}')
                exit(1)

            # check if destination path exists
            for sub in ["deployments", "templates", "parameters"]:
                destination_path = os.path.join(args.config_directory, sub)
                if not os.path.exists(destination_path):
                    print(f'destination path: {destination_path} does not exist, did you run tjcli init?')
                    exit(1)

            # copy all files from template
            for sub in ["deployments", "templates", "parameters"]:
                template_final_dir = os.path.join(template_named_dir, sub)
                destination_path = os.path.join(args.config_directory, sub)

                # check if template has sub dir
                if os.path.exists(template_final_dir):
                    for filename in os.listdir(template_final_dir):
                        destination_file = os.path.join(destination_path, filename)
                        print(f'dest: {destination_file}')
                        if os.path.exists(destination_file) and not args.force:
                            print(f'file {destination_file} already exists, aborting. use --force to overwrite')
                            exit(1)

                    for filename in os.listdir(template_final_dir):
                        print(f'adding: {sub} / {filename}')
                        shutil.copyfile(os.path.join(template_final_dir, filename), os.path.join(destination_path, filename))

