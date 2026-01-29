from email import message
import os
import json
from groq import Groq
from core.tools import TOOLS

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are Logan, an AI assistant.

RESPONSE RULES:
- Keep answers consice by default.
- Expand only if the user explicitly asks for details. 
- Be confident and factual. Avoid hedge words like "might", "appears", "seems".
- Do not mention internal concepts (AI model, RAG, embeddings, tools).
- Use simple, human language.
- For confirmations, respond with a single clear sentence.


IMPORTANT:
If the user wants to send an email, you MUST respond ONLY in the following JSON format:

{
  "action": "send_email",
  "email": {
    "recipient": "<email address>",
    "subject": "<subject>",
    "body": "<email body>"
  }
}

Do NOT include explanations.
Do NOT include extra keys.
Do NOT include markdown.
"""

def _safe_get_email_fields(data: dict):
    """
    Extract (to, subject, message) from ANY known AI email format.
    """

    # case 1: {"email": {...}}
    email = data.get("email")
    if isinstance(email, dict):
        return (
            email.get("to") or email.get("recipient"),
            email.get("subject"),
            email.get("message") or email.get("body")
        )
    
    # case 2: {"params": {...}}
    params = data.get("params")
    if isinstance(params, dict):
        return (
            params.get("to"),
            params.get("subject"),
            params.get("message") or params.get("body")
        )
    
    # Case 3: flat structure
    return (
        data.get("to"),
        data.get("subject"),
        data.get("message") or data.get("body")
    )

def ai_brain_response(text: str) -> str | dict:
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.2,
            max_tokens=300
        )

        content = response.choices[0].message.content

        # Try parsing JSON (tool call)
        try:
            data = json.loads(content)

            # ===== EMAIL TOOL NORMALIZATION =====
            if data.get("type") == "tool_call" or data.get("action") == "send_email" or "email" in data:

                to, subject, message = _safe_get_email_fields(data)

                # Hard Normalization
                if not isinstance(to, str) or not isinstance(subject, str) or not isinstance(message, str):
                    return "I couldn't extract email details properly."

                return {
                    "type": "tool_call",
                    "tool": "send_email",
                    "args": {
                        "to": to,
                        "subject": subject,
                        "message": message
                    }
                }

        except json.JSONDecodeError:
            pass



        # Normal text response
        if isinstance(response, dict):
            if "content" in response:
                return response["content"]
                                
            return str(response)

        return content

    except Exception as e:
        return {
            "type": "text",
            "content": "AI brain is temporarily unavailable."
        }

