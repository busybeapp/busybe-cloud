import logging
from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException, status

from .model.entry import Entry
from .persistence.entries_store import EntriesStore

logger = logging.getLogger(__name__)
router = APIRouter()
persistence = EntriesStore()


@router.post("/", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_entry(
        entry: Entry
):
    logger.info(f"Received entry data: {entry.dict()}")
    persisted_entry = persistence.add_entry(entry.dict())
    return persisted_entry.to_json()


@router.get("/", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
def get_entries():
    logger.info("Fetching all entries")
    try:
        entries = persistence.get_entries()
        logger.info(f"Retrieved entries: {entries}")
        return entries
    except Exception as e:
        logger.error(f"Error retrieving entries: {e}")
        raise HTTPException(status_code=500, detail=str(e))
