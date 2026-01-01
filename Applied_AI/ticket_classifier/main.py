import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Support Ticket Classifier API")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-key-here"))

class TicketRequest(BaseModel):
    ticket_text: str

class TicketResponse(BaseModel):
    tags: List[str]
    priority: str
    suggested_action: str

SYSTEM_PROMPT = """
You are a support ticket triage assistant. 
Classify the incoming ticket text into tags (e.g., billing, technical, feature request, account) and assign a priority (Low, Medium, High, Urgent).
Provide a concise suggested next action.
Return JSON format.
"""

@app.get("/")
async def root():
    return {"message": "Support Ticket Classifier API is running"}

@app.post("/classify", response_model=TicketResponse)
async def classify_ticket(request: TicketRequest):
    if not os.getenv("OPENAI_API_KEY"):
         # Mock response if key is missing for demonstration
         return TicketResponse(
             tags=["technical"],
             priority="Medium",
             suggested_action="Assign to technical support team for further investigation."
         )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.ticket_text},
            ],
            response_format={ "type": "json_object" }
        )
        return TicketResponse(**eval(response.choices[0].message.content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
