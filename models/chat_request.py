from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    npc_id: str
    user_text: str