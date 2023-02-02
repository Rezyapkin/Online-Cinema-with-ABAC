from fastapi import APIRouter, status

from api import healthcheck as health_route
from api import v1 as v1_route

router = APIRouter(responses={status.HTTP_404_NOT_FOUND: {"description": "Page not found"}})

router.include_router(v1_route.router, prefix="/v1")
router.include_router(health_route.router, prefix="/healthcheck", tags=["Internal"])
