from komodo.framework.komodo_tool import KomodoTool


class KomodoToolRegistry:
    REGISTRY = {}

    @classmethod
    def add_tool(cls, shortcode: str, definition: dict, action: callable):
        cls.REGISTRY[shortcode] = KomodoTool(shortcode=shortcode,
                                             definition=definition,
                                             action=action)

    @classmethod
    def get_tool_by_shortcode(cls, shortcode: str) -> KomodoTool:
        return cls.REGISTRY.get(shortcode)

    @classmethod
    def get_tools(cls, shortcodes) -> [KomodoTool]:
        if shortcodes is None:
            return []

        result = [cls.REGISTRY[sc] for sc in shortcodes if sc in cls.REGISTRY]
        missing_tools = [sc for sc in shortcodes if sc not in cls.REGISTRY]
        for sc in missing_tools:
            print(f"Requested tool {sc} not found in registry")
        return result

    @classmethod
    def get_definitions(cls, tools):
        definitions = []
        for t in tools or []:
            if isinstance(t, str):
                definitions.append(KomodoToolRegistry.get_tool_by_shortcode(t).definition)
            elif isinstance(t, dict) and 'definition' in t:
                definitions.append(t['definition'])
            elif isinstance(t, KomodoTool):
                definitions.append(t.definition)
            else:
                raise ValueError(f"Invalid tool: {t}")
        return definitions
