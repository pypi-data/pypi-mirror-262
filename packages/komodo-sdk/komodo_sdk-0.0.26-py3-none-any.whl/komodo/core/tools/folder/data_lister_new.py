import base64
import json
from pathlib import Path

from komodo.framework.komodo_datasource import default_data_directory
from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.shared.utils.filestats import file_details


class DataLister(KomodoTool):
    name = "Data Lister"
    purpose = "Lists data files and returns directory contents in base64 encoded string. " + \
              "You should decode the string to get the original data which contains a list of files with their details."
    shortcode = "data_lister"

    definition = {
        "type": "function",
        "function": {
            "name": name,
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

    def __init__(self):
        super().__init__(shortcode=self.shortcode,
                         definition=self.definition,
                         action=self.action)

    def action(self, args):
        try:
            # Adjust the path as needed
            datadir = default_data_directory()
            pattern = args.get("pattern", "*")
            files = self.get_files_recursively_pathlib(datadir, pattern)
            result = []

            for file in files:
                details = file_details(str(file))
                file_info = {
                    "file": str(file),
                    "namw": details.name,
                    "type": details.magic,
                    "checksum": details.checksum,
                    "created_at": details.created_at,
                    "updated_at": details.modified_at
                }
                result.append(file_info)

            print(result)

            result_json = json.dumps(result)  # Convert result to JSON string
            result_bytes = result_json.encode('utf-8')  # Convert JSON string to bytes
            base64_encoded_result = base64.b64encode(result_bytes)  # Encode as base64
            return base64_encoded_result.decode('ascii')

        except Exception as e:
            print("Failed to list files: ", e)
            return "Failed to list files: " + str(args.get("pattern", ""))

    def get_files_recursively_pathlib(self, datadir, pattern='*'):
        return Path(datadir).rglob(pattern)


if __name__ == "__main__":
    t = DataLister()
    print(t.definition)
    print(t.action({"pattern": "*.py"}))

    KomodoToolRegistry.add_tool(t.shortcode, t.definition, t.action)
    print(KomodoToolRegistry.get_definitions([t.shortcode]))
    y = KomodoToolRegistry.get_tool_by_shortcode(t.shortcode)
    print(y.definition)
    print(y.action({"pattern": "*.py"}))
