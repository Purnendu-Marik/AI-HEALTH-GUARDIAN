from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/api",
    tags=["Assessment"]
)


class HealthAssessment(BaseModel):
    age: int
    gender: str
    symptoms: list[str]
    sleep: str
    activity: str
    additional_info: str = ""


@router.post("/assessment")
async def submit_assessment(data: HealthAssessment):

    return {
        "success": True,
        "message": "Assessment received successfully!",
        "data": data.model_dump()
    }