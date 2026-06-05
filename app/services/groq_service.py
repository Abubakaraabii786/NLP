import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_contract(contract_text):

    prompt = f"""
You are a contract analysis expert.

Analyze the contract and return ONLY valid JSON.

Required JSON format:

{
  "contract_type":"",
  "parties":[],
  "effective_date":"",
  "expiration_date":"",
  "payment_terms":"",
  "auto_renewal":"",
  "summary":""
}

Contract:

{contract_text[:12000]}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown wrappers
    if content.startswith("```json"):
        content = content.replace("```json", "", 1)

    if content.startswith("```"):
        content = content.replace("```", "", 1)

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    try:
        return json.loads(content)

    except Exception as e:
        return {
            "error": str(e),
            "raw_response": content
        }
