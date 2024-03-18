from datetime import datetime

from komodo.models.azure.azure_openai import azure_assistant_response
from komodo.models.bedrock.bedrock_model import bedrock_assistant_response
from komodo.models.framework.assistant import ModelRequest, ModelResponse
from komodo.models.openai.openai_api import openai_chat_response


def get_model_response(request: ModelRequest) -> ModelResponse:
    start_time = datetime.now()
    if request.agent.provider is not None:
        if request.agent.provider == "openai":
            response = openai_chat_response(request)
        elif request.agent.provider == "azure":
            response = azure_assistant_response(request)
        elif request.agent.provider == "bedrock":
            response = bedrock_assistant_response(request)
        else:
            raise Exception("Unknown provider: " + request.agent.provider)
    else:
        raise Exception("No provider specified for assistant: " + request.agent.shortcode)

    response.started = start_time.timestamp()
    response.completed = datetime.now().timestamp()
    return response
