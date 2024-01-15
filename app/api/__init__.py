from fastapi import FastAPI, APIRouter
from .wallets.views import router as wallet_router

router = APIRouter()
router.include_router(router=wallet_router, prefix="/wallets")

api = FastAPI(title='NFT API', version='0.0.1')

