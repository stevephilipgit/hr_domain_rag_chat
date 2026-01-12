from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag import ask_question

app = FastAPI(title="Enterprise HR Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSIONS = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str
    intent: str
    sources: list

def get_memory(session_id: str):
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {"topic": None}
    return SESSIONS[session_id]

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    memory = get_memory(req.session_id)
    result = ask_question(req.message, memory)
    return ChatResponse(**result)
