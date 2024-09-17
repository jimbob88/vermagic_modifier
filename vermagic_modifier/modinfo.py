"""Functions related to interpreting data from '.modinfo' section."""
from typing import Iterator


def _generate_modinfo_content(modinfo_content: bytes) -> Iterator[tuple[str, str]]:
    key_val_pairs = [pair for pair in modinfo_content.split(b"\x00") if pair]
    for pair in key_val_pairs:
        key, val = pair.split(b"=")
        yield key.decode("utf-8"), val.decode("utf-8")


def modinfo_content_to_dict(modinfo_content: bytes) -> dict[str, str]:
    """Takes modinfo content and transforms key value pairs into decoded dict."""
    return dict(_generate_modinfo_content(modinfo_content))
