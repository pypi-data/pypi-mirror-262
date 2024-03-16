class KomodoTool:
    def __init__(self, shortcode, definition, action):
        self.shortcode = shortcode
        self.definition = definition
        self.action = action
        self.name = definition['function']['name']
        self.purpose = definition['function']['description']

    def __str__(self):
        return f"KomodoTool: {self.shortcode} {self.name} ({self.purpose})"

    def to_dict(self):
        return {
            'shortcode': self.shortcode,
            'name': self.name,
            'purpose': self.purpose,
            'definition': self.definition
        }

    def run(self, args: dict):
        return self.action(args)
