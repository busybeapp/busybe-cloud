import logging
from typing import List, Dict, Any

from fastapi import APIRouter, status, Depends

from .model.entry import Entry
from .persistence.entries_store import EntriesStore
from service.login import token

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(token.verify)])
persistence = EntriesStore()


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_entry(
        entry: Entry
):
    logger.info(f"Received entry data: {entry.model_dump()}")
    entry = persistence.add_entry(entry.model_dump())
    return entry.to_json()


@router.get("", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
def get_entries():
    return persistence.get_entries()
