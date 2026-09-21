from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Guidepost API")

class TroubleshootRequest(BaseModel):
    query: str
    siis_response: str = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/troubleshoot")
def troubleshoot(req: TroubleshootRequest):
    # To be implemented in Phase 4-6
    pass
