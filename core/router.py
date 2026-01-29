from commands.time_cmd import handle_time_command
from commands.date_cmd import handle_date_command
from commands.open_browser import handle as handle_browser_command
from commands.system_cmd import handle_system_command
from commands.battery_cmd import handle_battery_command
from commands.email_cmd import handle_email_command
from commands.memory_cmd import handle_memory_command
from commands.episodic_cmd import handle_episodic_command
from core.ai_brain import ai_brain_response 
from rag.qa import rag_answer
from rag.summarizer import summarize_pdf

def route(text: str):
    text = text.lower()

    if text in ["exit", "quit"]:
        return "exit"
    
    memory_response = handle_memory_command(text)
    if memory_response:
        return memory_response
    
    episodic_response = handle_episodic_command(text)
    if episodic_response:
        return episodic_response

    if "date" in text:
        return handle_date_command(text)

    if "time" in text:
        return handle_time_command(text)

    if "open browser" in text or "open google" in text:
        return handle_browser_command(text)
    
    if "system info" in text or "system information" in text or "system status" in text:
        return handle_system_command(text)
    
    if "battery" in text or "battery status" in text or "battery info" in text:
        return handle_battery_command(text)
    
    if "send email" in text:
        return handle_email_command(text)
    
    if "summarize" in text.lower():
        return summarize_pdf()
    
    # RAG-based question answering
    rag_triggers = ( 
        "what is", 
        "who is", 
        "tell me about", 
        "explain", 
        "search",
        "find"
        "look up"
    )

    if any(text.lower().startswith(t) for t in rag_triggers):
        return rag_answer(text)

    ai_response = ai_brain_response(text)
    if ai_response:
        return ai_response
    
    return "Okay"