# src/api.py
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uuid
from src.main import run_competitor_check, run_comparison
from src.database.memory import reset_memory

app = FastAPI(title="AI Competitor Analyst API")

# Simple in-memory storage for report status (replace with DB for production)
reports_db = {}

class ComparisonRequest(BaseModel):
    comp1: str
    url1: str
    comp2: str
    url2: str

def perform_analysis(request_id: str, comp1: str, url1: str, comp2: str, url2: str):
    """The background task that runs the actual CrewAI logic."""
    try:
        reset_memory()
        run_competitor_check(comp1, url1)
        run_competitor_check(comp2, url2)
        report = run_comparison(comp1, comp2)
        
        reports_db[request_id] = {"status": "completed", "report": report}
    except Exception as e:
        reports_db[request_id] = {"status": "failed", "error": str(e)}

@app.post("/analyze")
async def start_analysis(request: ComparisonRequest, background_tasks: BackgroundTasks):
    request_id = str(uuid.uuid4())
    reports_db[request_id] = {"status": "processing", "report": None}
    
    # Trigger the heavy AI work in the background
    background_tasks.add_task(
        perform_analysis, request_id, request.comp1, request.url1, request.comp2, request.url2
    )
    
    return {"job_id": request_id, "message": "Analysis started in background"}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    return reports_db.get(job_id, {"status": "not_found"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    