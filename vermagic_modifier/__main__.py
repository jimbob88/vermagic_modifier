"""Commandline tool for modifying vermagic data."""

import argparse
from importlib import metadata
from importlib.metadata import PackageMetadata


class ParseArgs:
    """Get values of arguments from command line."""

    def __init__(self, project_name="vermagic_modifier"):
        self._project_name = project_name
        self._parser = argparse.ArgumentParser(prog=self._project_name)
        self.add_arguments()

    def add_arguments(self):
        """Define which arguments are accepted by script."""
        self._parser.description = self.description
        self._parser.add_argument(
            "--version", action="version", version=self.version_string
        )

    @property
    def version_string(self) -> str:
        """The argparse versioning information."""
        return f"%(prog)s {self._get_version()}"

    @property
    def description(self) -> str:
        """The argparse description (same in toml file)."""
        return self._metadata.get("Summary", "No description given")

    @property
    def _metadata(self) -> PackageMetadata:
        """Information from pyproject toml."""
        return metadata.metadata(self._project_name)

    def _get_version(self):
        """Get the raw version, e.g. '1.0.0'."""
        return metadata.version(self._project_name)

    def parse_args(self) -> argparse.Namespace:
        """Get the namespace object from command line."""
        return self._parser.parse_args()


def get_args():
    """Wrap the arg parsing class to easily get args."""
    return ParseArgs().parse_args()


def main():
    """Commandline core logic."""
    get_args()


if __name__ == "__main__":
    main()
