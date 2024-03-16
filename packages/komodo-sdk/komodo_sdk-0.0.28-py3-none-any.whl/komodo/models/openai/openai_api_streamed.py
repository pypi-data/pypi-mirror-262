import openai
from openai.types.chat.completion_create_params import ResponseFormat

from komodo.core.tools.folder.data_lister_new import DataLister
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.models.framework.assistant import AssistantRequest
from komodo.models.framework.models import OPENAI_GPT4_MODEL, max_function_output_len
from komodo.models.openai.openai_api_streamed_tool_call import StreamingToolCallBuilder
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

    try:
        metadata['max_output_length'] = max_function_output_len(request.model()),
        for token in openai_invoke_streamed(client, request.prompt, request.model(),
                                            tools, messages, metadata, output_format):
            yield token

    except openai.BadRequestError as e:
        if e.code == "context_length_exceeded" and request.model() != OPENAI_GPT4_MODEL:
            metadata['max_output_length'] = max_function_output_len(OPENAI_GPT4_MODEL)
            for token in openai_invoke_streamed(client, request.prompt, OPENAI_GPT4_MODEL,
                                                tools, messages, metadata, output_format):
                yield token
        else:
            raise e

    except Exception as e:
        print(e)
        yield "Encountered error retrieving results: " + str(e)


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
    done = False
    while not done:
        completion = client.chat.completions.create(**params)
        streamed_role = None
        tool_call_builder = StreamingToolCallBuilder()
        for chunk in completion:
            delta = chunk.choices[0].delta
            if delta is not None:
                if delta.role is not None and delta.role != streamed_role:
                    streamed_role = delta.role
                if delta.content is not None:
                    yield delta.content
                if delta.tool_calls is not None:
                    tool_call_builder.process(delta.tool_calls)

        tool_calls = tool_call_builder.get_tool_calls()
        if tool_calls:
            outputs = process_actions_gpt_streaming(tools, metadata, tool_calls)
            for output in outputs:
                messages.append(output)

            params['messages'] = messages
        else:
            done = True


if __name__ == '__main__':
    from komodo.core.tools.web.tavily_search_tool import setup_tavily_search_action
    from komodo.core.tools.web.action_serpapi_search import setup_serpapi_search_action

    setup_tavily_search_action()
    setup_serpapi_search_action()
    client = openai_client()

    prompt = "list files available to you"
    for response in openai_invoke_streamed(client, prompt=prompt, tools=[DataLister()]):
        print(response, end="")
    print()

    prompt = "whats up in nyc today? search for event and then search for additional details on the first event found"
    # for response in openai_invoke_streamed(client, prompt=prompt, tools=["komodo_serpapi_search"]):
    #   print(response, end="")
    print()
