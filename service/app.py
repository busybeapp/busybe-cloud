import logging
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from service.entries.model.entry import Entry
from service.entries.persistence.driver import EntriesDriver
from service.entries.validators.validator import ResourceValidationError, validate_fields
from service.health.health_response import HealthResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

persistence = EntriesDriver()


class HealthResponseModel(BaseModel):
    status: str
    message: str


@app.exception_handler(ResourceValidationError)
async def resource_validation_exception_handler(request: Request, exc: ResourceValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )


@app.get("/api/health", response_model=HealthResponseModel, status_code=status.HTTP_202_ACCEPTED)
def health():
    logger.info("Health check requested")
    return HealthResponse().to_client()


@app.post("/api/entries", status_code=status.HTTP_201_CREATED)
async def create_entry(
        entry: Entry,
        validate: None = Depends(validate_fields(['title']))  # This ensures 'title' is validated
):
    logger.info(f"Received entry data: {entry.dict()}")
    persisted_entry = persistence.add_entry(entry.dict())
    return persisted_entry.to_json()


@app.get("/api/entries", response_model=List[Dict[str, Any]], status_code=status.HTTP_202_ACCEPTED)
def get_entries():
    logger.info("Fetching all entries")
    try:
        entries = persistence.get_entries()
        logger.info(f"Retrieved entries: {entries}")
        return entries
    except Exception as e:
        logger.error(f"Error retrieving entries: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("ENDPOINT", "localhost")
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host=host, port=port)
