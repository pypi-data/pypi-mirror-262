import base64
from typing import AsyncGenerator

from fastapi import Depends, APIRouter, HTTPException, Request
from starlette.responses import StreamingResponse

from komodo.models.framework.runners import run_agent, run_agent_streamed, get_agent
from komodo.server.globals import get_appliance, get_email_from_header
from komodo.store.conversations_store import ConversationStore

router = APIRouter(
    prefix='/api/v1/agent',
    tags=['Agent']
)


@router.api_route('/ask', methods=['POST'])
async def ask_agent(request: Request, email=Depends(get_email_from_header), appliance=Depends(get_appliance)):
    # Parse the request body as JSON
    body = await request.json()
    # Extract the message and agent_info fields from the JSON body
    message = body.get("message")
    agent_shortcode = body.get("agent_shortcode")
    if not message or not agent_shortcode:
        raise HTTPException(status_code=400, detail="Missing 'message or agent_shortcode' in request body")

    # Get Agent Info based on short code
    agent = get_agent(appliance, agent_shortcode)
    if agent is None:
        raise HTTPException(status_code=400, detail="Respective Agent is not available")

    store = ConversationStore()
    conversation = store.get_or_create_conversation(body.get("guid"), agent_shortcode, email, message)
    store.add_user_message(guid=conversation.guid, sender=email, text=message)
    history = store.get_history(conversation.guid)

    try:
        reply = run_agent(appliance, agent, message, history)
        store.add_agent_message(guid=conversation.guid, sender=agent_shortcode, text=reply.text)
        return {"reply": reply.text, "message": message}
    except Exception as e:
        print("Error while asking agent: ", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ask-streamed")
async def ask_agent_streamed(email: str, agent_shortcode: str, prompt: str, guid: str = None,
                             appliance=Depends(get_appliance)):
    print("email: ", email, "agent_shortcode: ", agent_shortcode, "prompt: ", prompt)

    # Get Agent Info based on short code
    agent = get_agent(appliance, agent_shortcode)
    if agent is None:
        raise HTTPException(status_code=400, detail="Respective Agent is not available")

    store = ConversationStore()
    conversation = store.get_or_create_conversation(guid, agent_shortcode, email, prompt)
    store.add_user_message(guid=conversation.guid, sender=email, text=prompt)
    history = store.get_history(conversation.guid)

    def stream_callback():
        try:
            return run_agent_streamed(appliance, agent, prompt, history)
        except Exception as e:
            print("Error while asking agent: ", e)
            raise HTTPException(status_code=500, detail=str(e))

    def store_callback(reply):
        store.add_agent_message(conversation.guid, sender=agent_shortcode, text=reply)

    return StreamingResponse(komodo_async_generator(stream_callback, store_callback),
                             media_type='text/event-stream')


async def komodo_async_generator(stream_callback, store_callback) -> AsyncGenerator[str, None]:
    reply = ""
    exception_occurred = False  # Flag to indicate an exception occurred during yield
    exception_message = ""  # To store the exception message
    for part in stream_callback():
        reply += part
        if exception_occurred:
            break  # Stop processing if an exception has occurred

        try:
            encoded = base64.b64encode(part.encode('utf-8')).decode('utf-8')
            yield f"data: {encoded}\n\n"
        except Exception as e:
            exception_occurred = True
            exception_message = str(e)

    store_callback(reply)

    if exception_occurred:
        print("Error while streaming: " + exception_message)
    else:
        print("stream complete")
        yield "event: stream-complete\ndata: {}\n\n"
