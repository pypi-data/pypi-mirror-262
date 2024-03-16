import base64
import os

from komodo.framework.komodo_datasource import default_data_directory
from komodo.framework.komodo_tool_registry import KomodoToolRegistry

DATA_READER_ACTION_NAME = "komodo_data_reader"


def data_reader_definition():
    return {
        "type": "function",
        "function": {
            "name": DATA_READER_ACTION_NAME,
            "description": 'Reads data files and returns contents as base64 encoded string. You should decode the string to get the original data.',
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of data file to read"
                    },
                },
                "required": ["filename"]
            }
        }
    }


def data_reader_action(args):
    try:
        datadir = default_data_directory()
        path = os.path.join(datadir, args["filename"])
        with open(path, 'rb') as file:
            return base64.b64encode(file.read()).decode('ascii')
    except Exception as e:
        print("Failed to read file: ", e)
        return "Failed to read file: " + args["filename"]


def setup_data_reader_action():
    KomodoToolRegistry.add_tool(DATA_READER_ACTION_NAME, data_reader_definition(), data_reader_action)
