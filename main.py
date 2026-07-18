from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware # NEW IMPORT
from llm_engine import generate_linkedin_post

app = FastAPI(title="LinkedIn Ghostwriter API")

# NEW: The CORS Bouncer
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, we restrict this. For local testing, "*" allows all.
    allow_credentials=True,
    allow_methods=["*"], # Allows POST, GET, etc.
    allow_headers=["*"], # Allows all headers
)

class PostRequest(BaseModel):
    topic: str

@app.get("/")
def read_root():
    return {"status": "Online"}

@app.post("/generate")
def create_post(request: PostRequest):
    return {"engaging_linkedin_post": generate_linkedin_post(request.topic)}