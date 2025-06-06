from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_active_user
from app.db.models.user import User
from app.schemas.strategy import Strategy, StrategyCreate, StrategyUpdate
from app.services.strategy import strategy_service

router = APIRouter()

@router.get("/", response_model=List[Strategy])
def read_strategies(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve strategies.
    """
    strategies = strategy_service.get_multi(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return strategies

@router.post("/", response_model=Strategy)
def create_strategy(
    *,
    db: Session = Depends(get_db),
    strategy_in: StrategyCreate,
    current_user: User = Depends(get_current_active_user),
):
    """
    Create new strategy.
    """
    strategy = strategy_service.create(
        db=db, obj_in=strategy_in, user_id=current_user.id
    )
    return strategy

@router.get("/{strategy_id}", response_model=Strategy)
def read_strategy(
    *,
    db: Session = Depends(get_db),
    strategy_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """
    Get strategy by ID.
    """
    strategy = strategy_service.get(db=db, strategy_id=strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if strategy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return strategy

@router.put("/{strategy_id}", response_model=Strategy)
def update_strategy(
    *,
    db: Session = Depends(get_db),
    strategy_id: int,
    strategy_in: StrategyUpdate,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a strategy.
    """
    strategy = strategy_service.get(db=db, strategy_id=strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if strategy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    strategy = strategy_service.update(db=db, db_obj=strategy, obj_in=strategy_in)
    return strategy

@router.delete("/{strategy_id}", response_model=Strategy)
def delete_strategy(
    *,
    db: Session = Depends(get_db),
    strategy_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a strategy.
    """
    strategy = strategy_service.get(db=db, strategy_id=strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if strategy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    strategy = strategy_service.delete(db=db, db_obj=strategy)
    return strategy

