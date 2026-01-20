import yaml
from pathlib import Path

def read_yaml(path_to_yaml: Path):
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    return content

def create_directories(path_to_directories: list):
    for path in path_to_directories:
        Path(path).mkdir(parents=True, exist_ok=True)