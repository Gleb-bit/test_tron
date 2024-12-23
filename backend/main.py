from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError, DBAPIError

from exc_handlers.base import (
    value_error_handler,
    related_errors_handler,
    input_error_handler,
)
from views import query_router

app = FastAPI(title="Test tron app")

exc_handlers = {
    DBAPIError: input_error_handler,
    IntegrityError: related_errors_handler,
    ValueError: value_error_handler,
}
routers = {
    "/queries": query_router
}

for exception, handler in exc_handlers.items():
    app.add_exception_handler(exception, handler)

for prefix, router in routers.items():
    app.include_router(router, prefix=prefix)
