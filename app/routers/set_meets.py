from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from config.supabase import supabase

router = APIRouter(
    prefix="/setmeets",
    tags=['SetMeets']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_pairmeets():

    response = supabase.table('users_pair_meets').select("*").execute()
 
    return response