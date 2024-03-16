import uvicorn
from fastapi import FastAPI
from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from .logging import configure_logger
from .logging import loggingMiddleware
from .utils import get_project_data

tags_metadata = []

app_name, app_version = get_project_data()


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


@app.get("/")
async def base(request: Request):
    logger.info(request.state.req_id)
    return {"status": "ok"}


def main():
    uvicorn.run(
        f"zeph1rr_fastapi_utils.__main__:app",
        host="localhost",
        port=8080,
        reload=True,
    )


if __name__ == "__main__":
    main()
