from .metadata import SetMetadataString, SetMetadataAll, SetMetadataFloat

NODE_CLASS_MAPPINGS = {
    "SetMetadataString": SetMetadataString,
    "SetMetadataAll": SetMetadataAll,
    "SetMetadataFloat": SetMetadataFloat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SetMetadataString": "Set Metadata (String)",
    "SetMetadataAll": "Set Metadata (All)",
    "SetMetadataFloat": "Set Metadata (Float)",
}

__version__ = "0.1.1"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
