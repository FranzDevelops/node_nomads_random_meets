from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from config.supabase import supabase
from app.events_for_pairs import create_pairs_events

router = APIRouter(
    prefix="/setmeets",
    tags=['SetMeets']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_pair_meets():

    create_pairs_events()
 
    return {
        "status": "success"
    }