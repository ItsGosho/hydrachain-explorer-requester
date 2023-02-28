import toml

version = toml.load("pyproject.toml")["project"]["version"]

__version__ = version
