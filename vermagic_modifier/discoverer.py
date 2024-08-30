"""Scrape modinfo from a kernel module."""
import typing

from elftools.elf import elffile


class ModInfoDiscoverer:
    """Gets information from the ELF modfile section in an LKM."""

    def __init__(self, streamable: typing.BinaryIO):
        self._streamable = streamable
        self._elffile = elffile.ELFFile(streamable)

    def get_section(self, section_name: str):
        """Wraps elffile get section, raising a value error if fails.

        :param section_name: section name (generally preceded by '.', e.g. '.modinfo')
        :return: elffile section object
        """
        section = self._elffile.get_section_by_name(section_name)
        if section is None:
            raise ValueError(f"Section {section_name} not found in {self._elffile}")

        return section

    def get_modinfo_data(self):
        """Gets bytes representation from modinfo."""
        modinfo_section = self.get_section(".modinfo")
        return modinfo_section.data()
