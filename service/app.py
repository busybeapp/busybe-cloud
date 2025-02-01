import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from service.entries import router as entries_router
from service.health import router as health_router
from service.slack import router as slack_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


app.include_router(health_router.router, prefix="/health")
app.include_router(entries_router.router, prefix="/api/entries")
app.include_router(slack_router.router, prefix="/api/slack/message-shortcut")


@app.middleware("http")
async def enforce_trailing_slash(request: Request, call_next):
    if not request.url.path.endswith("/") and request.url.path != "/":
        return RedirectResponse(url=f"{request.url.path}/", status_code=301)
    return await call_next(request)


def main():
    import uvicorn
    host = os.getenv("ENDPOINT", "localhost")
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
