from fastapi import FastAPI, Header, HTTPException
from snowflake.snowpark import Session
import os

app = FastAPI(title="Snowflake Backend API")

def get_session():
    return Session.builder.getOrCreate()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ask")
def ask(
    q: str,
    x_api_key: str = Header(None)
):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")

    session = get_session()

    df = session.sql(f"""
        SELECT *
        FROM TABLE(
            CORTEX_ANALYST(
                'SHIVANSHI_SEMANTIC_VIEW',
                '{q}'
            )
        )
    """)

    return {
        "question": q,
        "result": df.to_pandas().to_dict(orient="records")
    }
