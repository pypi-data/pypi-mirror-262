import os
from pathlib import Path

from komodo.framework.komodo_datasource import default_data_directory
from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.shared.utils.filestats import file_details


class DirectoryReader(KomodoTool):
    name = "Directory Reader"
    purpose = "Lists directory contents recursively in base64 encoded string. " + \
              "Decode the base64 string to get the list of files with their details."
    shortcode = "komodo_directory_reader"

    definition = {
        "type": "function",
        "function": {
            "name": shortcode,
            "description": purpose,
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Pattern of files to match. Defaults to all files if not provided."
                    },
                }
            }
        }
    }

    def __init__(self, directory=default_data_directory()):
        super().__init__(shortcode=self.shortcode,
                         definition=self.definition,
                         action=self.action)
        self.directory = directory

    def action(self, args):
        try:
            pattern = args.get("pattern", "*")
            files = self.get_files_recursively_pathlib(self.directory, pattern)
            result = []

            for file in files:
                if os.path.isfile(file):
                    details = file_details(str(file))
                    file_info = {
                        "file": str(file),
                        "name": details.name,
                        "type": details.magic,
                        "checksum": details.checksum,
                        "created_at": details.created_at,
                        "updated_at": details.modified_at
                    }
                    result.append(file_info)

            print(result)
            return KomodoTool.to_base64(result)

        except Exception as e:
            print("Failed to list files: ", e)
            return "Failed to list files: " + str(args.get("pattern", ""))

    def get_files_recursively_pathlib(self, datadir, pattern='*'):
        return Path(datadir).rglob(pattern)


if __name__ == "__main__":
    t = DirectoryReader()
    print(t.definition)
    print(t.action({"pattern": "*.py"}))

    KomodoToolRegistry.add_tool(t.shortcode, t.definition, t.action)
    print(KomodoToolRegistry.get_definitions([t.shortcode]))
    y = KomodoToolRegistry.get_tool_by_shortcode(t.shortcode)
    print(y.definition)
    print(y.action({"pattern": "*.py"}))
