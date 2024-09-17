"""Scrape vermagic information from a kernel module."""
import logging
import pathlib

from pybfd3 import bfd

from vermagic_modifier import modinfo

logger = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class VermagicDiscover:
    """Gets elf section information from a lkm."""

    def __init__(self, kernel_module: pathlib.Path):
        self._kernel_module = kernel_module
        self._bfd = bfd.Bfd(str(kernel_module))
        logger.info("Linux Kernel Module File Format: %s", self._bfd.file_format_name)

    def _get_sections(self) -> dict[str, bfd.BfdSection]:
        """Gets elf/dwarf sections from the lkm."""
        return self._bfd.sections

    def _get_modinfo(self) -> bfd.BfdSection:
        """Gets the modinfo section from the lkm, raising KeyError on fail."""
        return self._get_sections()[".modinfo"]

    def get_modinfo_content(self) -> dict[str, str]:
        """Gets the modinfo section content as a dictionary of key value pairs."""
        return modinfo.modinfo_content_to_dict(self._get_modinfo().content)
