from fastapi import APIRouter, HTTPException, Depends, Request

import json
from google.protobuf import json_format

from komodo.server.globals import get_appliance, get_email_from_header
from komodo.store.collection_store import CollectionStore

router = APIRouter(
    prefix='/api/v1/collections',
    tags=['Collections']
)

@router.post('/')
async def create_collection(request: Request, email=Depends(get_email_from_header), appliance=Depends(get_appliance)):
    # Parse the request body as JSON
    body = await request.json()
    collection_name = body.get("collection")
    description = body.get("description")
    guid = body.get("guid") or ''
    if not collection_name:
        raise HTTPException(status_code=400, detail="Missing 'collection_name' in Request")

    collections_store = CollectionStore()
    collection = collections_store.get_or_create_collection(guid, collection_name, description)
    user_collection = collections_store.add_user_collection(email,collection.guid)
    collection_dict = json.loads(json_format.MessageToJson(collection))
    return collection_dict

