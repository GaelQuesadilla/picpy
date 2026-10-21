import tomllib
from pathlib import Path

base = Path.cwd()
assets = base / "src" / "picpy" / "assets"

with open(base / "config.toml", "rb") as config_file:
    config = tomllib.load(config_file)


with open(base / "pyproject.toml", "rb") as project_file:
    project = tomllib.load(project_file)


def is_dark():
    mode = config["GUI"]["mode"]
    return mode == "dark"


if __name__ == "__main__":
    import pprint
    pprint.pprint(config)
    pprint.pprint(project)
