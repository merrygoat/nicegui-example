import pathlib

import yaml


def load_config(config_location: pathlib.Path = "config.yaml"):
    with open(config_location, 'r') as input_file:
        return yaml.safe_load(input_file)


CONFIG = load_config()
