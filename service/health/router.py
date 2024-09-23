import logging

from fastapi import APIRouter, status

from service.health.model.health import Health

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=Health, status_code=status.HTTP_200_OK)
def health():
    logger.info("Health check requested")
    return Health().to_client()
