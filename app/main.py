import json
import logging
import os

import uvicorn
from datadog import initialize, statsd
from fastapi import FastAPI
from redisrpc import RedisRPC

from app.crud.routers.dealers import router as dealers_router
from app.crud.routers.info import router as info_router
from app.crud.routers.vehicles import router as vehicles_router

initialize(statsd_host=os.environ.get('DATADOG_HOST'))

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(dealers_router, prefix="/dealers", tags=["dealers"])
app.include_router(vehicles_router, prefix="/vehicles", tags=["vehicles"])
app.include_router(info_router)

rpc_inst = RedisRPC(os.getenv("REDISRPC_CHANNEL"))


@app.get("/rpc/{number}")
def rpc(number: int):
    statsd.increment('fastapi.views.rpc')
    result = rpc_inst.send("rpc", json.dumps({"key": number}))
    return {"message": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
