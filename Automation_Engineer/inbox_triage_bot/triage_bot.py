import os
import json
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-key-here"))

class EmailTriage(BaseModel):
    category: str
    priority: str
    route_to: str
    summary: str

def triage_email(email_body):
    system_prompt = """
    You are an Ops Inbox Triage Bot.
    Classify the email into: [Sales, Support, Partnerships, Spam].
    Assign priority: [Low, Medium, High].
    Route to: [CRM, Zendesk, Slack, Trash].
    Provide a 1-sentence summary.
    Return JSON.
    """
    
    if not os.getenv("OPENAI_API_KEY"):
        return EmailTriage(
            category="Sales",
            priority="High",
            route_to="CRM",
            summary="Potential lead inquiring about enterprise pricing."
        )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": email_body}
        ],
        response_format={ "type": "json_object" }
    )
    
    return EmailTriage(**json.loads(response.choices[0].message.content))

if __name__ == "__main__":
    sample_email = "Hi team, I'm interested in your premium plan for 50 users. Can we hop on a call? - John from Acme Corp"
    result = triage_email(sample_email)
    print(f"Classification: {result.category}")
    print(f"Routing: {result.route_to}")
    print(f"Summary: {result.summary}")
