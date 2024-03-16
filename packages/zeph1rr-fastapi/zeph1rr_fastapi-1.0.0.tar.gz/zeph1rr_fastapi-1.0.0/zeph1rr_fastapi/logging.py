import datetime
import json
import sys
import time
from enum import Enum
from typing import Callable
from uuid import UUID
from uuid import uuid4

from fastapi import Request
from fastapi import Response
from loguru import logger
from pydantic import BaseModel
from starlette.concurrency import iterate_in_threadpool


class LogType(str, Enum):
    request = "REQUEST"
    response = "RESPONSE"


class Log(BaseModel):
    request_id: UUID
    type: LogType


class RequestLog(Log):
    method: str
    path: str
    body: str

    def __str__(self):
        return f"({self.request_id}) {self.type.value} {self.method} - {self.path} - {json.dumps(self.body, ensure_ascii=False)}"


class ResponseLog(Log):
    status_code: int
    request_time_duration: datetime.time
    error: str | None

    def __str__(self):
        return f"({self.request_id}) {self.type.value} {self.status_code} - {self.request_time_duration} - {self.error}"


def configure_logger(
    log_level: str = "DEBUG",
    logger_format: str = "{time:YYYY-MM-DD HH:mm:ss.SSS} - [{level}] {message}",
):
    """Configuring logger for app

    Arguments

    log_level -- loguru log level (default 'DEBUG')

    logget_format -- format for logging (default '{time:YYYY-MM-DD HH:mm:ss.SSS} - [{level}] {message}')"""
    logger.remove()
    logger.add(sys.stdout, level=log_level, colorize=True, format=logger_format)


async def loggingMiddleware(request: Request, call_next: Callable) -> Response:
    """Middleware for requests logging

    Adding uuid req_id to request.state for easy parsing logs"""
    start_time = time.time()
    request_id = uuid4()
    req_body = await request.body()
    request_log_data = {
        "request_id": request_id,
        "type": "REQUEST",
        "method": request.method,
        "path": request.url.path,
        "body": req_body.decode("utf-8"),
    }
    request.state.req_id = request_id
    logger.info(str(RequestLog(**request_log_data)))
    response: Response = await call_next(request)
    response_log_data = {
        "request_id": request_id,
        "type": "RESPONSE",
        "status_code": response.status_code,
        "request_time_duration": time.time() - start_time,
        "error": None,
    }
    if response.status_code != 200:
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        if len(response_body):
            response_body = json.loads(response_body[0].decode())
            logger.error(f'({request_id}) {response_body["detail"]}')
            response_log_data["error"] = response_body
    logger.info(str(ResponseLog(**response_log_data)))
    return response
