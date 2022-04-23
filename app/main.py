from fastapi import Depends, FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import app.controllers.channels_articles as channels_articles_controller
import app.models.api as api_models
import app.services.database as database
from app.services.authentication import verify_api_token

API_RESPONSES = {
    status.HTTP_400_BAD_REQUEST: {"model": api_models.Error},
    status.HTTP_403_FORBIDDEN: {"model": api_models.Error},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "n/a"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": api_models.Error},
}

fastapi_app = FastAPI(
    title="Channel and Articles API",
    description="API to access channels and articles resources",
    responses=API_RESPONSES,
    openapi_url="/local/openapi.json",
    dependencies=[Depends(verify_api_token)],
)

fastapi_app.include_router(
    channels_articles_controller.router, tags=["Channels Articles"]
)


@fastapi_app.on_event("startup")
def startup_event():
    database.connect_to_db()
    database.create_table()


@fastapi_app.on_event("shutdown")
def shutdown_event():
    database.close_connection()


# Used to generate openapi
@fastapi_app.get("/openapi.json", include_in_schema=False)
def get_openapi():
    return fastapi_app.openapi()


@fastapi_app.exception_handler(RequestValidationError)
def request_validation_exception_handler(request, e):
    return JSONResponse({"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)


@fastapi_app.exception_handler(Exception)
def exception_handler(request, e):
    return JSONResponse(
        {"message": str(e).splitlines()},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
