from uuid import UUID

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from loguru import logger
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from .logging import configure_logger
from .logging import loggingMiddleware
from .models import BaseRequestData
from .models import ResponseData
from .utils import get_project_data

tags_metadata = []

app_name, app_version = get_project_data()
app_name = app_name.replace("-", "_")


def lifespan(_):
    configure_logger()
    logger.debug(f"Application {app_name}:{app_version} successfully started")
    yield
    logger.debug(f"Application {app_name}:{app_version} successfully stoped")


app = FastAPI(
    title=app_name,
    description="Бекенд приложения autoiinovatic",
    version=app_version,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

app.add_middleware(BaseHTTPMiddleware, dispatch=loggingMiddleware)


class CheckIdData(BaseModel):
    name: str


class ReqData(BaseRequestData):
    data: CheckIdData


@app.get("/")
async def base(request: Request):
    logger.info(request.state.req_id)
    return {"status": "ok"}


@app.post("/")
async def check_id(req_data: ReqData, request: Request):
    return ResponseData(
        data={
            "req_id_success": str(req_data.req_id) == str(request.state.req_id),
            "name": req_data.data.name,
        },
        error=False,
    )


@app.get("/{path:path}")
async def check(request: Request):
    return ResponseData(
        data={"req_id": request.state.req_id, "path": request.url.path}, error=False
    )


def main():
    uvicorn.run(
        f"{app_name}.__main__:app",
        host="localhost",
        port=8080,
        reload=True,
    )


if __name__ == "__main__":
    main()
