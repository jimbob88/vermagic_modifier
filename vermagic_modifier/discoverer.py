"""Scrape vermagic information from a kernel module."""
import logging
import pathlib

from pybfd3 import bfd

logger = logging.getLogger(__name__)


class VermagicDiscover:
    """Gets elf section information from a lkm."""

    def __init__(self, kernel_module: pathlib.Path):
        self._kernel_module = kernel_module
        self._bfd = bfd.Bfd(str(kernel_module))
        logger.info("Linux Kernel Module File Format: %s", self._bfd.file_format_name)

    def get_sections(self) -> dict[str, bfd.BfdSection]:
        """Gets elf/dwarf sections from the lkm."""
        return self._bfd.sections

    def get_modinfo(self) -> bfd.BfdSection:
        """Gets the modinfo section from the lkm, raising KeyError on fail."""
        return self.get_sections()[".modinfo"]
