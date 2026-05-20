from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import uvicorn
import os

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Request body
class ChatRequest(BaseModel):
    message: str

# Home route
@app.get("/")
def home():

    return {
        "message": "Emotion Companion Backend Running"
    }

# Chat route
@app.post("/chat")
def chat(req: ChatRequest):

    response = client.chat.completions.create(

        model="deepseek/deepseek-chat-v3-0324",

        messages=[
            {
                "role": "system",
                "content": """
                You are a supportive emotional AI companion.
                Speak calmly, warmly, and empathetically.
                """
            },
            {
                "role": "user",
                "content": req.message
            }
        ]
    )

    ai_response = response.choices[0].message.content

    return {
        "response": ai_response
    }

# Run server
if __name__ == "__main__":

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )