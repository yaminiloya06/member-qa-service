from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os
import re
from fireworks.client import Fireworks


app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}


fireworks_client = Fireworks(api_key=os.getenv("FIREWORKS_API_KEY"))



EXTERNAL_MESSAGES_URL = "https://november7-730026606190.europe-west1.run.app/messages/"

async def fetch_messages():
    """
    Fetch messages from the public API.
    Handles redirects (307/302) automatically.
    """
    async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
        try:
            response = await client.get(EXTERNAL_MESSAGES_URL)
            response.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

    data = response.json()
    return data["items"]     



def llm_qa(question: str, messages):
    """
    Use Fireworks Llama-3.1-70B to answer questions.
    The model is restricted to ONLY use the provided messages.
    """
    system_prompt = """
    You are a precise question-answering assistant.
    You must answer ONLY using the member messages provided.
    If the answer is not found, respond exactly with:
    "I couldn't find an answer based on the member messages."
    Never guess, never hallucinate, never create fake facts.
    """

    user_prompt = f"""
    Here are the member messages as JSON:

    {json.dumps(messages, indent=2)}

    QUESTION: {question}

    Give a short, direct answer.
    """

    response = fireworks_client.chat.completions.create(
        model="accounts/fireworks/models/llama-v3p1-70b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()




class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str



@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
   
    messages = await fetch_messages()

 
    answer = llm_qa(req.question, messages)

   
    return AskResponse(answer=answer)
