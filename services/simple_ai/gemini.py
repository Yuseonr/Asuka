from services.simple_ai.persona import ASUKA_PERSONA
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client()

async def asuka_response(prompt: str) -> str:
    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=ASUKA_PERSONA + prompt,
        )
        return response.text
        
    except Exception as e:
        return f"Ugh, my brain lagged, fix your code, yus.. Error: {e}"
