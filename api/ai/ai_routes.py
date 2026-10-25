from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.ai_query_service import answer_query, AIQueryError
from logger_config import logger

router = APIRouter(prefix="/api/ai", tags=["AI"])


class AIQueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        examples=["Which store had the highest total sales?"],
    )


@router.post("/query")
def ai_query(request: AIQueryRequest):
    """
    Ask a plain-English question about the retail data (products, sales,
    stores, customers, inventory). The AI converts it into a read-only
    SQL query, runs it, and returns both the data and a short answer.

    Examples:
      - "What are the top 5 best-selling products?"
      - "Which store had the most sales last month?"
      - "How many products are below their reorder level?"
    """
    logger.info(f"POST /api/ai/query called: {request.question}")

    try:
        return answer_query(request.question)
    except AIQueryError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error in AI query: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error processing AI query")
