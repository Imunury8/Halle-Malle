from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv
import os

# Groq API 키
client = Groq(api_key=os.getenv("GROQ_API_KEY1"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_text: str

@app.post("/ask")
async def ask_ai(request: ChatRequest):
        
        
    
        chat = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": request.user_text
                }
            ],
            model="llama-3.1-8b-instant"
        )

        answer = chat.choices[0].message.content

        return {"answer": answer}

    

  