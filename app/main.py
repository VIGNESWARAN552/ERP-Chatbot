from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import process_message  # Make sure your folder structure supports this import
import logging



# Initialize FastAPI app
app = FastAPI()

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Define request and response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Add CORS middleware to allow frontend requests (update URL if your frontend runs elsewhere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Change if your frontend URL differs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the ERP chatbot API"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        logging.info(f"Received message: {req.message}")
        reply = await process_message(req.message)
        logging.info(f"Generated reply: {reply}")
        return ChatResponse(reply=reply)
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
