import os

from komodo.framework.komodo_tool import KomodoTool


class FileReader(KomodoTool):
    shortcode = "komodo_file_reader"
    name = "File Reader"
    purpose = "Reads data files and returns contents as base64 encoded string. You must decode the results."

    definition = {
        "type": "function",
        "function": {
            "name": shortcode,
            "description": purpose,
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of file to read"
                    },
                },
                "required": ["filename"]
            }
        }
    }

    def __init__(self, path):
        super().__init__(shortcode=self.shortcode,
                         definition=self.definition,
                         action=self.action)
        self.path = path

    def action(self, args):
        try:
            path = os.path.join(self.path, args["filename"])
            with open(path, 'rb') as file:
                contents = file.read()
                return KomodoTool.to_base64(contents)
        except Exception:
            return "Failed to read file: " + args["filename"]


if __name__ == "__main__":
    from komodo.testdata.config import TestConfig

    tool = FileReader(TestConfig.path("dir1"))
    print(tool.definition)
    print(tool.action({"filename": "hello.txt"}))
