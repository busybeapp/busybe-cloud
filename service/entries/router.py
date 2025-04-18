import logging
from typing import List, Dict, Any

from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from .model.entry import Entry
from .persistence.entries_store import EntriesStore
from ..login import token

logger = logging.getLogger(__name__)
router = APIRouter()
persistence = EntriesStore()


def extract_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    return credentials.credentials


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_entry(
        entry: Entry,
        access_token: str = Depends(extract_token)
):
    logger.info(f"Received entry data: {entry.model_dump()}")
    token.verify(access_token)
    entry = persistence.add_entry(entry.model_dump())
    return entry.to_json()


@router.get("", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
def get_entries(
        access_token: str = Depends(extract_token)
):
    token.verify(access_token)
    return persistence.get_entries()
