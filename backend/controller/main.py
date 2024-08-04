import traceback
from typing import Literal

from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from commons.db import client, initialize_records
from commons.logger import logger
from commons.exceptions import BlackCofferException
from services.auth_service import AuthenticationService
from models.record import RecordFilterRequestModel, PaginatedRecordsResponse

from services.data_service import DataService

from contextlib import asynccontextmanager

TAGS_METADATA = [
    {
        "name": "Records",
        "description": "Records related operations"
    },
    {
        "name": "Health",
        "description": "Health check apis"
    }
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On Start
    on_app_startup(app)
    yield
    # On End
    on_app_exit(app)

def on_app_startup(app: FastAPI):
    initialize_records()

def on_app_exit(app: FastAPI):
    client.close()

app = FastAPI(title="Blackcoffer Backend", description="API for Blackcoffer", version="1.0.0", openapi_tags=TAGS_METADATA, lifespan=lifespan)

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:*",
    "http://localhost:3000",
    "http://localhost:*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


@app.post("/api/records", dependencies=[Depends(AuthenticationService)], tags=["Records"], response_model=PaginatedRecordsResponse)
def records(filters: RecordFilterRequestModel, page: int = 1, count: int = 10):
    return DataService().get_records(count, page, filters)

@app.post("/api/distinct", dependencies=[Depends(AuthenticationService)], tags=["Records"], response_model=list)
def distinct(filters: RecordFilterRequestModel, param: Literal['sector', 'topic', 'insight', 'region', 'country', 'pestle', 'source', 'title']):
    return DataService().get_distinct(param, filters)

@app.exception_handler(BlackCofferException)
async def handle_application_exceptions(request: Request, exc: BlackCofferException):
    trace = traceback.format_exc()
    logger.error(f'handle_application_exceptions: {trace}')
    raised_exc = HTTPException(
        status_code=exc.status_code or status.HTTP_503_SERVICE_UNAVAILABLE, detail=exc.detail())
    return await http_exception_handler(request, raised_exc)


@app.exception_handler(HTTPException)
async def handle_http_exceptions(request: Request, exc: HTTPException):
    trace = traceback.format_exc()
    logger.error(f'handle_http_exceptions: {trace}')
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def handle_validation_errors(request: Request, exc: RequestValidationError):
    trace = traceback.format_exc()
    logger.error(f'handle_validation_errors: {trace}')
    response = await request_validation_exception_handler(request, exc)
    return response


@app.exception_handler(Exception)
def handle_unhandled_exceptions(request: Request, exc: Exception):
    logger.warn(f'Error caught {exc.__class__.__name__}')
    if isinstance(exc, BlackCofferException):
        return handle_application_exceptions(request, exc)
    elif isinstance(exc, HTTPException):
        return handle_http_exceptions(request, exc)
    elif isinstance(exc, RequestValidationError):
        return handle_validation_errors(request, exc)
    trace = traceback.format_exc()
    logger.error(f'handle_unhandled_errors: {trace}')
    return http_exception_handler(request, HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Experienced Downtime"))