from fastapi import Depends, APIRouter, HTTPException

from komodo.models.framework.appliance_runtime import ApplianceRuntime
from komodo.server.globals import get_appliance

router = APIRouter(
    prefix='/api/v1/appliance',
    tags=['Appliance']
)


@router.get('/description', response_model=dict, summary='Get appliance description',
            description='Get the description of the appliance.')
def get_appliance_description(appliance=Depends(get_appliance)):
    if not appliance:
        raise HTTPException(status_code=404, detail="Appliance not found")

    runtime = ApplianceRuntime(appliance)
    agents = runtime.get_all_agents()
    return {
        "shortcode": appliance.shortcode,
        "name": appliance.name,
        "purpose": appliance.purpose,
        "agents": [a.to_dict() for a in agents]
    }


@router.get('/index', summary='Index all data sources',
            description='Index all data sources for the appliance.')
def index_all_data_sources(appliance=Depends(get_appliance)):
    if not appliance:
        raise HTTPException(status_code=404, detail="Appliance not found")
    appliance.index(reindex=False)
    return {"status": "success"}


@router.get('/reindex', summary='Re-index all data sources.',
            description='Deletes all existing data and re-indexes all data sources for the appliance.')
def re_index_all_data_sources(appliance=Depends(get_appliance)):
    if not appliance:
        raise HTTPException(status_code=404, detail="Appliance not found")

    appliance.index(reindex=True)
    return {"status": "success"}
