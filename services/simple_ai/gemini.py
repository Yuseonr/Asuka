from services.simple_ai.persona import ASUKA_PERSONA, SYSTEM_PROMPT
from services.simple_ai.memory import load_history, save_history
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client()
chat_archive = None

async def asuka_response(prompt: str) -> str:
    global chat_archive

    if chat_archive is None:
        chat_archive = await load_history()

    recent_context = chat_archive[-6:] if len(chat_archive) > 0 else []
    chat_history = "{CHAT HISTORY}\n"
    chat_history += "\n".join(recent_context)
    

    if not chat_history:
        chat_history = "[No previous conversation history.]"

    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=ASUKA_PERSONA+'\n' + SYSTEM_PROMPT+ '\n' + chat_history +'\n' + "User: " + prompt,
        )

        reply = response.text.strip()
        chat_archive.append(f"User: {prompt}")
        chat_archive.append(f"Asuka: {reply}")
        await save_history(chat_archive)

        return reply
        
    except Exception as e:
        return f"Ugh, my brain lagged, fix your code, yus.. Error: {e}"
