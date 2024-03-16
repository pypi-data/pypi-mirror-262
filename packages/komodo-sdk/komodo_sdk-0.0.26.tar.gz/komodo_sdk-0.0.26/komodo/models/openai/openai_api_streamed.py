import json

from openai.types.chat import ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function
from openai.types.chat.completion_create_params import ResponseFormat
from pydantic import ValidationError

from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.models.framework.assistant import AssistantRequest
from komodo.models.framework.models import OPENAI_GPT4_MODEL
from komodo.models.openai.openai_completion import openai_client
from komodo.models.openai.openai_process_actions import process_actions_gpt_streaming
from komodo.shared.utils.sentry_utils import sentry_trace


def openai_chat_response_streamed(request: AssistantRequest):
    client = openai_client()
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

    for token in openai_invoke_streamed(client, request.prompt, request.model(),
                                        tools, messages, metadata, output_format):
        yield token


@sentry_trace
def openai_invoke_streamed(client, prompt, model=OPENAI_GPT4_MODEL, tools=None, messages=None, metadata=None,
                           output_format=None):
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

    params['stream'] = True
    completion = client.chat.completions.create(**params)
    tool_calls = []
    streamed_role = None

    tool_call_accumulator = ""  # Accumulator for JSON fragments of tool call arguments
    tool_call_id = None  # Current tool call ID
    function_name = None

    for chunk in completion:
        delta = chunk.choices[0].delta
        if delta is not None:
            if delta.role is not None and delta.role != streamed_role:
                streamed_role = delta.role
            if delta.content is not None:
                yield delta.content
            if delta.tool_calls is not None:
                for tc in chunk.choices[0].delta.tool_calls:
                    if tc.id:  # New tool call detected here
                        tool_call_id = tc.id
                        tool_call_accumulator = ""
                    if tc.function.name:
                        function_name = tc.function.name
                    tool_call_accumulator += tc.function.arguments if tc.function.arguments else ""
                    try:
                        json.loads(tool_call_accumulator)
                        fn = Function(name=function_name, arguments=tool_call_accumulator)
                        tool_calls.append(ChatCompletionMessageToolCall(id=tool_call_id, function=fn, type='function'))
                    except json.JSONDecodeError:
                        pass
                    except ValidationError as ve:
                        print(ve)
                        pass

    if tool_calls:
        outputs = process_actions_gpt_streaming(tools, metadata, tool_calls)
        for output in outputs:
            messages.append(output)

        params['messages'] = messages
        params['tools'] = None
        completion = client.chat.completions.create(**params)
        streamed_role = None
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta is not None:
                if delta.role is not None and delta.role != streamed_role:
                    streamed_role = delta.role
                if delta.content is not None:
                    yield delta.content


if __name__ == '__main__':
    from komodo.core.tools.web.tavily_search_tool import setup_tavily_search_action
    from komodo.core.tools.web.action_serpapi_search import setup_serpapi_search_action

    setup_tavily_search_action()
    setup_serpapi_search_action()
    client = openai_client()
    for response in openai_invoke_streamed(client, prompt="whats up in nyc today?", tools=["komodo_serpapi_search"]):
        print(response, end="")
    print()
