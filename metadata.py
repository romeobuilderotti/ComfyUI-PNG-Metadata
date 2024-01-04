import comfy

class ParametersUpdater:

    SET_PARAMETERS = True
    
    def update_parameters(self, params_string: str, name: str, value) -> str:
        """Modify the a1111 compatible (mostly) parameters string to include the new parameter
        
        Parameters format:
        <Prompt>
        [Negative prompt: <Negative prompt>]
        [Steps: <steps>, Seed: <seed>, ...]
        """
        prompt, *other = params_string.split("\n") + [""] * 3
        negative = None
        params = None
        for item in other:
            if item:
                if item.startswith("Negative prompt: "):
                    negative = item
                else:
                    params = item

        if name.lower() == "prompt":
            prompt = value
        elif name.lower() in ("negative prompt", "negative"):
            negative = f"Negative prompt: {value}"
        else:
            if isinstance(value, str) and any(c in value for c in (',', '\n', '"')):
                value = '"' + value.replace('"', '\\"') + '"'
            if params:
                params += f", {name}: {value}"
            else:
                params = f"{name}: {value}"
            
        return "\n".join(filter(None, [prompt, negative, params]))

class SetMetadataFloat(ParametersUpdater):
    """
    Set a single custom metadata field and optionally update 'parameters' field in png metadata
    """
    CATEGORY = "utils"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "process"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {}),
                "value": ("FLOAT", {"forceInput": True, "default": 0}),
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    def process(self, name: str, value: float = 0, update_parameters: bool = True, extra_pnginfo=None):
        if extra_pnginfo is not None and name and value:
            extra_pnginfo[name] = value
            if self.SET_PARAMETERS and name != "parameters":
                extra_pnginfo["parameters"] = self.update_parameters(extra_pnginfo.get("parameters", ""), name, value)
        return (None,)

class SetMetadataString(ParametersUpdater):
    """
    Set a single custom metadata field and optionally update 'parameters' field in png metadata
    """
    CATEGORY = "utils"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "process"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "name": ("STRING", {}),
                "value": ("STRING", {"forceInput": True, "default": ""}),
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    def process(self, name: str, value: str = "", update_parameters: bool = True, extra_pnginfo=None):
        if extra_pnginfo is not None and name and value:
            extra_pnginfo[name] = value
            if self.SET_PARAMETERS and name != "parameters":
                extra_pnginfo["parameters"] = self.update_parameters(extra_pnginfo.get("parameters", ""), name, value)
        return (None,)

class SetMetadataAll(SetMetadataString):
    """
    Set multiple metadata at once and write them to 'parameters' field in png metadata
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "prompt": ("STRING", {"forceInput": True, "default": None}),
                "negative": ("STRING", {"forceInput": True, "default": None}),
                "model_name": ("STRING", {"forceInput": True, "default": None}),
                "steps": ("INT", {"forceInput": True, "default": None}),
                "cfg": ("FLOAT", {"forceInput": True, "default": None}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, {"forceInput": True, "default": None}),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"forceInput": True, "default": None}),
                "seed": ("INT", {"forceInput": True, "default": None}),
            },
            "hidden": {
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }
    
    def process(self, **kwargs):
        extra_pnginfo = kwargs.pop("extra_pnginfo", None)
        if extra_pnginfo is not None:
            params = extra_pnginfo.get("parameters", "")
            for k, v in kwargs.items():
                if v is not None:
                    params = self.update_parameters(params, self.convert_name(k), self.convert_value(v))
            if params:
                extra_pnginfo["parameters"] = params
        return (None,)
    
    def convert_name(self, name: str) -> str:
        names_dict = {
            "prompt": "Prompt",
            "negative": "Negative prompt",
            "model_name": "Model",
            "steps": "Steps",
            "seed": "Seed",
            "cfg": "CFG scale",
            "sampler_name": "Sampler",
            "scheduler": "Scheduler",
        }
        return names_dict.get(name, name)
    
    def convert_value(self, value):
        return value