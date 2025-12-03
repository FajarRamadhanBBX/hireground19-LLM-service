import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY tidak ditemukan.")

genai.configure(api_key=API_KEY)

def generate_reply(prompt, history, user_text):
    # Menggunakan model Flash agar lebih cepat
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=prompt
    )
    
    chat = model.start_chat(history=history)
    
    response = chat.send_message(user_text)
    
    return response.text