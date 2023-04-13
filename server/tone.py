from fastapi import APIRouter
from pydantic import BaseModel

router=APIRouter()
#formalize, professional, 
@router.post("/tone/professional")
def make_professional(data):
    pass
