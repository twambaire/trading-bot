from fastapi import APIRouter

from app.api.endpoints import auth, users, strategies, backtests, trading

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(strategies.router, prefix="/strategies", tags=["strategies"])
api_router.include_router(backtests.router, prefix="/backtests", tags=["backtests"])
api_router.include_router(trading.router, prefix="/trading", tags=["trading"])

