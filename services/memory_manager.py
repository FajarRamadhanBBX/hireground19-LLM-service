import time
from services import session_manager

def get_history(session_id: str):
    current_time = time.time()
    session = session_manager.get_session(session_id)
    if session is not None:
        session_manager.set_session_data(session_id, 'last_access', current_time)
        return session.get('history', [])
    if session is None:
        raise ValueError("Session ID tidak valid.")
    return []

def add_history(session_id: str, role: str, text: str):
    current_time = time.time()
    session = session_manager.get_session(session_id)
    if session is None:
        raise ValueError("Session ID tidak valid.")
    entry = {'role': role, 'parts': [text]}
    history = session.get('history', [])
    history.append(entry)
    print("history: " + str(history))
    if len(history) > 10:
        history.pop(0)
    session_manager.set_session_data(session_id, 'history', history)
    session_manager.set_session_data(session_id, 'last_access', current_time)