import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.common.logger import log
from app.config.nacos_config import get_nacos_client, get_config

router = APIRouter(prefix="/nacos", tags=['nacos'])

"""
get nacos configuration
"""
@router.get(path="/getConfig", summary="get nacos configuration", description="Read the latest configuration information from the Nacos service and return it in JSON format.")
def get_nacos_config():
    result = get_config()
    log.info(f"get the latest configuration results of nacos:{json.dumps(result)}")
    return JSONResponse(content=result)


"""
refresh nacos configuration
"""

@router.post(path='/refresh', summary="refresh nacos configuration", description="Manually trigger the Nacos client refresh operation to obtain the latest configuration.")
def refresh_nacos_config():
    nacos_client = get_nacos_client()
    nacos_client.refresh()
    if nacos_client is None:
        return JSONResponse(content={"message": "Nacos client not initialized"}, status_code=500)

    result = nacos_client.get_yaml_config()
    log.info(f"get the latest configuration results of nacos:{json.dumps(result)}")
    return JSONResponse(content=result)
