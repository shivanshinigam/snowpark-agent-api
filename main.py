from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from snowflake.snowpark import Session

app = FastAPI(title="Snowpark Agent Public API")

class QuestionRequest(BaseModel):
    question: str

def get_session():
    return Session.builder.getOrCreate()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: QuestionRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")

    session = get_session()

    sql = f"""
        SELECT *
        FROM TABLE(
            CORTEX_AGENT(
                'SHIVANSHI_AGENT',
                '{req.question}'
            )
        )
    """

    try:
        df = session.sql(sql)
        return {
            "question": req.question,
            "answer": df.to_pandas().to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
