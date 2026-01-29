from voice.listen import listen_once
from voice.speak import speak
from core.router import route
from core.ai_brain import ai_brain_response
from core.tools import TOOLS

def should_speak(text: str) -> bool:
    blacklist = (
        "i don't have",
        "i couldn't find",
        "i ran into",
        "error"
    )

    t = text.lower()
    if any(b in t for b in blacklist):
        return False
    
    if len(text) > 200:
        return False
    if "\n" in text:
        return False
    return True

def run():
    print("Logan: Ready when you are.")
    speak("Ready when you are.")

    while True:
        text = listen_once()

        if not text:
            continue

        if "exit" in text:
            speak("Goodbye.")
            break

        #Hard rules first
        result = route(text)
        if isinstance(result, str) and result.strip():
            print(f"Logan: {result}")
            voice_text = result
            if len(result) > 120:
                voice_text = result.split(".")[0] # first sentence only

            if should_speak(result):
                speak(voice_text)
            continue
        #AI Brain
        ai_response = ai_brain_response(text)

        # Tool call handling
        if isinstance(ai_response, dict) and ai_response.get("type") == "tool_call":
            tool_name = ai_response["tool"]
            args = ai_response.get("args", {})

            if tool_name in TOOLS:
                tool_entry = TOOLS[tool_name]
                handler = tool_entry["handler"]
                result = handler(**args)

                print(f"Logan: {result}")
                voice_text = result
                if len(result) > 120:
                    voice_text = result.split(".")[0] # first sentence only

                if should_speak(result):
                    speak(voice_text)
            else:
                print(f"Logan: Tool '{tool_name}' not found.")
                speak(f"Tool {tool_name} not found.")

            continue

        # Normal AI response
        if isinstance(ai_response, str) and ai_response.strip():
            print(f"Logan: {ai_response}")
            speak(ai_response)
            continue
        

if __name__ == "__main__":
    run()
