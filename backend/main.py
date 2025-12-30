from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, engine, Base
from models import CodeReview, Vulnerability
from agents.graph import app_graph

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/review")
async def start_code_review(filename: str, code: str, language: str, db: AsyncSession = Depends(get_db)):

    initial_state = {"code": code, "language": language}
    result = await app_graph.ainvoke(initial_state)
    
    new_review = CodeReview(
        filename=filename,
        original_code=code,
        refactored_code=result["refactored_code"],
        documentation=result["docs"]
    )
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    
    return {
        "id": new_review.id,
        "refactored": result["refactored_code"],
        "vulnerabilities": result["vulnerabilities"],
        "docs": result["docs"]
    }

