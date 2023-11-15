from .metadata import SetMetadataString, SetMetadataAll

NODE_CLASS_MAPPINGS = {
    "SetMetadataString": SetMetadataString,
    "SetMetadataAll": SetMetadataAll,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SetMetadataString": "Set Metadata",
    "SetMetadataAll": "Set Metadata (All)",
}

__version__ = "0.1.0"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
