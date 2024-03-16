from openai.types.chat.completion_create_params import ResponseFormat

from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.models.framework.assistant import AssistantRequest, AssistantResponse
from komodo.models.framework.models import OPENAI_GPT4_MODEL
from komodo.models.openai.openai_completion import openai_client
from komodo.models.openai.openai_process_actions import process_actions_gpt_legacy_api


def openai_chat_response(request: AssistantRequest) -> AssistantResponse:
    return openai_chat_response_with_client(openai_client(), request)


def openai_chat_response_with_client(client, request: AssistantRequest) -> AssistantResponse:
    messages = request.prepare_messages()
    tools = request.tools()
    metadata = {}
    if request.user:
        metadata['user_id'] = request.user['email']
        metadata['name'] = request.user['name']
    if request.assistant:
        metadata['agent_id'] = request.assistant['shortcode']

    output_format = None
    if request.assistant and 'output_format' in request.assistant:
        output_format = request.assistant['output_format']

    return openai_invoke(client, request.prompt, request.model(), tools, messages, metadata, output_format)


def openai_invoke(client, prompt, model=OPENAI_GPT4_MODEL, tools=None, messages=None, metadata=None,
                  output_format=None) -> AssistantResponse:
    response = invoke_text_model(client, model, prompt,
                                 tools=tools,
                                 messages=messages,
                                 metadata=metadata,
                                 output_format=output_format)
    text = response.choices[0].message.content
    status = response.choices[0].finish_reason
    return AssistantResponse(model=model, status=status, output=response, text=text)


def invoke_text_model(client, model, prompt, tools=None, messages=None, metadata=None, output_format=None):
    messages = messages or []
    messages.append({'role': 'user', "content": prompt})
    params = {
        "model": model,
        "messages": messages
    }

    if tools and len(tools) > 0:
        params['tools'] = KomodoToolRegistry.get_definitions(tools)

    if output_format and len(output_format) > 0 and 'json' in output_format:
        params['response_format'] = ResponseFormat(type="json_object")

    response = client.chat.completions.create(**params)
    response_message = response.choices[0].message
    messages.append(response_message)

    tool_calls = response_message.tool_calls
    while tool_calls:
        metadata = metadata or {}
        metadata['run_id'] = response.id
        outputs = process_actions_gpt_legacy_api(tools, metadata, tool_calls)
        for output in outputs:
            messages.append(output)

        params['messages'] = messages
        response = client.chat.completions.create(**params)
        response_message = response.choices[0].message
        messages.append(response_message)
        tool_calls = response_message.tool_calls

    return response


if __name__ == '__main__':
    client = openai_client()
    response = openai_invoke(client, prompt="whats up in nyc today?", tools=["komodo_tavily_search"])
    print(response.text)
