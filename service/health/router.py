from fastapi import APIRouter, status

from service.health.model.health import Health

router = APIRouter()


@router.get("/", response_model=Health, status_code=status.HTTP_200_OK)
def health():
    return Health().to_client()
