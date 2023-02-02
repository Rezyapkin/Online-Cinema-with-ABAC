from pydantic import BaseModel


class Healthcheck(BaseModel):
    cache_alive: bool
    db_alive: bool

    class Config:
        schema_extra = {
            "example": {
                "cache_alive": True,
                "db_alive": True,
            }
        }
