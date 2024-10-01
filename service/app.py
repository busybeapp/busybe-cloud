import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from service.entries import router as entries_router
from service.health import router as health_router
from service.slack import router as slack_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


app.include_router(health_router.router, prefix="/health")
app.include_router(entries_router.router, prefix="/api/entries")
app.include_router(slack_router.router, prefix="/api/slack/events")


def main():
    import uvicorn
    host = os.getenv("ENDPOINT", "localhost")
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
