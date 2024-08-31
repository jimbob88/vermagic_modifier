"""Replaces an LKM's vermagic string."""


def _encode_modinfo_dict(mod_info_dict: dict[str, str]) -> dict[bytes, bytes]:
    """Encodes the modinfo strings into utf-8 bytes objects."""
    return {
        bytes(key, "utf-8"): bytes(value, "utf-8")
        for key, value in mod_info_dict.items()
    }


def serialize_modinfo_dict(modinfo_dict: dict[str, str]) -> bytes:
    """Serialize modinfo into a bytes-like sequence"""
    modinfo_encoded = b"\x00".join(
        bytes(f"{key}={value}", "utf-8") for key, value in modinfo_dict.items()
    )
    return modinfo_encoded + b"\x00"
