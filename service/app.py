import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from service.entries import router as entries_router
from service.entries.validators.validator import ResourceValidationError
from service.health import router as health_router
from service.slack import router as slack_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()


@app.exception_handler(ResourceValidationError)
async def resource_validation_exception_handler(request: Request, exc: ResourceValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )

app.include_router(health_router.router, prefix="/api/health")
app.include_router(entries_router.router, prefix="/api/entries")
app.include_router(slack_router.router, prefix="/api/slack/events")

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("ENDPOINT", "localhost")
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host=host, port=port)
