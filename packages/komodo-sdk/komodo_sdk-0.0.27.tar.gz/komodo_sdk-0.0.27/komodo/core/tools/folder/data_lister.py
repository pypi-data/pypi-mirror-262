import base64
import json
import os
from datetime import datetime
from pathlib import Path

import magic

from komodo.framework.komodo_datasource import default_data_directory
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.shared.utils.digest import get_digest

DATA_LISTER_ACTION_NAME = "komodo_data_lister"


def data_lister_definition():
    return {
        "type": "function",
        "function": {
            "name": DATA_LISTER_ACTION_NAME,
            "description": 'Lists data files and returns directory contents in base64 encoded string. You should decode the string to get the original data which contains a list of files with their details.',
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


def get_files_recursively_pathlib(datadir, pattern='*'):
    return Path(datadir).rglob(pattern)


def data_lister_action(args):
    try:
        # Adjust the path as needed
        datadir = default_data_directory()
        pattern = args.get("pattern", "*")
        files = get_files_recursively_pathlib(datadir, pattern)
        result = []

        for file in files:
            if os.path.isfile(file):
                file_type = magic.from_file(str(file), mime=True)
                checksum = get_digest(file)
                created_at = datetime.fromtimestamp(file.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                updated_at = datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')

                file_info = {
                    "file": str(file),
                    "type": file_type,
                    "checksum": checksum,
                    "created_at": created_at,
                    "updated_at": updated_at
                }
                result.append(file_info)

        result_json = json.dumps(result)  # Convert result to JSON string
        result_bytes = result_json.encode('utf-8')  # Convert JSON string to bytes
        base64_encoded_result = base64.b64encode(result_bytes)  # Encode as base64
        return base64_encoded_result.decode('ascii')

    except Exception as e:
        print("Failed to list files: ", e)
        return "Failed to list files: " + str(args.get("pattern", ""))


def setup_data_lister_action():
    KomodoToolRegistry.add_tool(DATA_LISTER_ACTION_NAME, data_lister_definition(), data_lister_action)


if __name__ == "__main__":
    print(data_lister_action({}))
