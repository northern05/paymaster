from contextlib import asynccontextmanager
from app.core.config import config
from fastapi import FastAPI
from app.core.models import db_helper, Base
from app.api import router as router_v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=config.api_v1_prefix)