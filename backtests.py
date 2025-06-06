from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_active_user
from app.db.models.user import User
from app.schemas.backtest import Backtest, BacktestCreate, BacktestResults
from app.services.backtest import backtest_service
from app.services.backtester import backtester_service

router = APIRouter()

@router.get("/", response_model=List[Backtest])
def read_backtests(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve backtests.
    """
    backtests = backtest_service.get_multi(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return backtests

@router.post("/", response_model=Backtest)
def create_backtest(
    *,
    db: Session = Depends(get_db),
    backtest_in: BacktestCreate,
    current_user: User = Depends(get_current_active_user),
):
    """
    Create new backtest.
    """
    backtest = backtest_service.create(
        db=db, obj_in=backtest_in, user_id=current_user.id
    )
    return backtest

@router.get("/{backtest_id}", response_model=Backtest)
def read_backtest(
    *,
    db: Session = Depends(get_db),
    backtest_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """
    Get backtest by ID.
    """
    backtest = backtest_service.get(db=db, backtest_id=backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    if backtest.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return backtest

@router.delete("/{backtest_id}", response_model=Backtest)
def delete_backtest(
    *,
    db: Session = Depends(get_db),
    backtest_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a backtest.
    """
    backtest = backtest_service.get(db=db, backtest_id=backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    if backtest.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    backtest = backtest_service.delete(db=db, db_obj=backtest)
    return backtest

@router.post("/{backtest_id}/run", response_model=BacktestResults)
def run_backtest(
    *,
    db: Session = Depends(get_db),
    backtest_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """
    Run a backtest.
    """
    backtest = backtest_service.get(db=db, backtest_id=backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    if backtest.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    try:
        results = backtester_service.run_backtest(db=db, backtest_id=backtest_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{backtest_id}/results", response_model=BacktestResults)
def read_backtest_results(
    *,
    db: Session = Depends(get_db),
    backtest_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """
    Get backtest results.
    """
    backtest = backtest_service.get(db=db, backtest_id=backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    if backtest.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if not backtest.results:
        raise HTTPException(status_code=404, detail="Backtest results not found")
    
    return backtest.results

@router.get("/{backtest_id}/report")
def read_backtest_report(
    *,
    db: Session = Depends(get_db),
    backtest_id: int,
    current_user: User = Depends(get_current_active_user),
):
    """
    Get backtest report.
    """
    backtest = backtest_service.get(db=db, backtest_id=backtest_id)
    if not backtest:
        raise HTTPException(status_code=404, detail="Backtest not found")
    if backtest.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    if not backtest.results:
        raise HTTPException(status_code=404, detail="Backtest results not found")
    
    try:
        report = backtester_service.generate_report(db=db, backtest_id=backtest_id)
        return Response(content=report, media_type="text/html")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

