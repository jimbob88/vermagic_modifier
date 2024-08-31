"""Commandline tool for modifying vermagic data."""

import argparse
import logging
import pathlib
from importlib import metadata

from vermagic_modifier import discoverer, modifier

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(name)s %(levelname)s: %(message)s"
)


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
        self._parser.add_argument(
            "modfile",
            action="store",
            type=pathlib.Path,
            help="A Linux Kernel Module File (e.g. lib80211.ko)",
        )
        self._parser.add_argument(
            "new_vermagic",
            action="store",
            type=str,
            help="The replacement vermagic (e.g. '5.15.0-119-generic SMP mod_unload modversions')",
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
    def _metadata(self) -> metadata.PackageMetadata:
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
    args = get_args()
    modfile: pathlib.Path = args.modfile
    logger.info("Analysing vermagic info in %s", modfile)

    with modfile.open("rb") as binary_modstreamable:
        modinfo_data = discoverer.ModInfoDiscoverer(
            binary_modstreamable
        ).get_modinfo_data()

    logger.debug("Loaded RAW modinfo data: %s", modinfo_data)
    modinfo_dict = discoverer.parse_modinfo_data(modinfo_data)
    logger.info("Loaded modinfo data: %s", modinfo_dict)

    if "vermagic" in modinfo_dict:
        logger.info("Current vermagic: '%s'", modinfo_dict["vermagic"])
    else:
        logger.warning("No existing vermagic in modinfo, adding anyway.")

    logger.info("Setting vermagic to '%s'", args.new_vermagic)
    modinfo_dict["vermagic"] = args.new_vermagic

    logger.info("New modinfo data: %s", modinfo_dict)

    serialised = modifier.serialize_modinfo_dict(modinfo_dict)

    logger.debug("New RAW modinfo data: %s", serialised)


if __name__ == "__main__":
    main()
