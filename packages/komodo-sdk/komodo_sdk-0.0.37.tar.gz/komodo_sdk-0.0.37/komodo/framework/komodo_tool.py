import base64
import json


class KomodoTool:
    def __init__(self, shortcode, definition, action):
        self.shortcode = shortcode
        self.definition = definition
        self.action = action
        self.name = definition['function']['name']

    def __str__(self):
        return f"KomodoTool: {self.shortcode} {self.name} ({self.definition['function']['description']})"

    def to_dict(self):
        return {
            'shortcode': self.shortcode,
            'name': self.name,
            'definition': self.definition
        }

    def run(self, args: dict):
        return self.action(args)

    @staticmethod
    def to_base64(contents):
        result = {"Base64 Encoded": KomodoTool.to_base64_raw(contents)}
        return json.dumps(result)

    @staticmethod
    def to_base64_raw(contents):
        if type(contents) is bytes:
            return base64.b64encode(contents).decode('utf-8')

        if type(contents) is dict or type(contents) is list:
            v = json.dumps(contents, default=str)
            return base64.b64encode(v.encode('utf-8')).decode('utf-8')

        return base64.b64encode(str(contents).encode('utf-8')).decode('utf-8')

    @classmethod
    def default(cls):
        return KomodoTool(shortcode="test", definition={"function": {"name": "test", "description": "test"}},
                          action=lambda x: x)


if __name__ == "__main__":
    print(KomodoTool(shortcode="test", definition={"function": {"name": "test", "description": "test"}},
                     action=lambda x: x).to_dict())

    print(KomodoTool.to_base64("test"))
    print(KomodoTool.to_base64(b"test"))
    print(KomodoTool.to_base64({"test": "test"}))
    print(KomodoTool.to_base64([1, 2, 3]))
    print(KomodoTool.to_base64(1))
    print(KomodoTool.to_base64(1.0))
