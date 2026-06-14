from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import uvicorn
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Emotion Companion Backend Running"}

@app.post("/chat")
def chat(req: ChatRequest):

    prompt = f"""
You are a supportive emotional AI companion.
Speak calmly, warmly, and empathetically.

User:
{req.message}
"""

    response = model.generate_content(prompt)

    return {
        "response": response.text
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)