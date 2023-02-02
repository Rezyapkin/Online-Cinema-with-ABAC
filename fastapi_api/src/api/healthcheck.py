from fastapi import APIRouter, Depends

from api.schemas.healthcheck import Healthcheck
from services.healthcheck import get_healthcheck_service, HealthcheckService

router = APIRouter()


@router.get(
    "/",
    response_model=Healthcheck,
    summary="Состояние приложения",
    description="Состояние приложения",
    response_description="Состояние компонентов приложения",
    tags=["Internal"],
)
async def healthcheck(service: HealthcheckService = Depends(get_healthcheck_service)) -> Healthcheck:
    health = await service.healthcheck()
    return Healthcheck(
        db_alive=health.base_storage_alive,
        cache_alive=health.cache_alive,
    )
