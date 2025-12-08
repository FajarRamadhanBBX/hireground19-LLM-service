import json
import os
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from models.chat_request import ChatRequest
from models.chat_response import ChatResponse
from services import memory_manager, prompt_builder, gemini_client, session_manager

npc_data = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load data NPC
    global npc_data
    with open("data/npc_profiles_final.json", "r") as f:
        npc_data = json.load(f)
    print("NPC berhasil dimuat!")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "HireGround AI Service berjalan."}

@app.get("/api/create-session")
async def create_session():
     session_id = session_manager.generate_session_id()
     print("session_id: ", session_id)
     return session_id

@app.post("/api/delete-session/{session_id}")
async def delete_session(session_id: str):
    session_manager.cleanup_expired_sessions()
    success = session_manager.delete_session(session_id)
    if success:
        return {"status": "Sesi berhasil dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Session ID tidak ditemukan.")

@app.post("/api/llm-query", response_model=ChatResponse)
async def query_llm(request: ChatRequest):
    session_id = request.session_id
    npc_id = request.npc_id
    get_session = session_manager.is_valid_session(session_id)
    # print("get_session: ", get_session)
    if not get_session:
        raise HTTPException(status_code=400, detail="Membutuhkan session_id! Buatlah terlebih dahulu.")

    # Validasi NPC ID
    if npc_id not in npc_data:
        raise HTTPException(status_code=404, detail="NPC ID tidak ditemukan.")

    profile = npc_data[npc_id]

    # Ambil History Chat sebelumnya (per NPC)
    history = memory_manager.get_history(session_id, npc_id)
    all_sessions = session_manager.get_all_sessions()
    
    # Menyiapkan prompt
    prompt = prompt_builder.build_prompt(profile, request.user_text)

    try:
        # Panggil Gemini
        print("History: ", history)
        answer = gemini_client.generate_reply(prompt, history, request.user_text)

        # Simpan percakapan baru ke history (per NPC)
        memory_manager.add_history(session_id, npc_id, "user", request.user_text)
        memory_manager.add_history(session_id, npc_id, "model", answer)
        # print("All Sessions:", all_sessions)

        return ChatResponse(
            npc_id=npc_id,
            answer_text=answer
        )

    except Exception as e:
        print(f"Error Gemini: {e}")
        return ChatResponse(
            npc_id=npc_id,
            answer_text="Maaf, koneksi saya sedang gangguan. Bisa ulangi?"
        )