from pydantic import BaseModel

class ChatResponse(BaseModel):
    npc_id: str
    answer_text: str