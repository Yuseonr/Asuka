import os
import json
import aiofiles

DATA_FILE = f"services/simple_ai/memory.json"
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

async def load_history() -> list:
    if os.path.exists(DATA_FILE):
        async with aiofiles.open(DATA_FILE, 'r') as f:
            content = await f.read()
            return json.loads(content)
    return []

async def save_history(history: list):
    async with aiofiles.open(DATA_FILE, 'w') as f:
        await f.write(json.dumps(history, indent=4))

