import time
from services import session_manager

def get_history(session_id: str, npc_id: str):
    current_time = time.time()
    session = session_manager.get_session(session_id)
    if session is not None:
        session_manager.set_session_data(session_id, 'last_access', current_time)
        history_dict = session.get('history', {})
        return history_dict.get(npc_id, [])
    if session is None:
        raise ValueError("Session ID tidak valid.")
        return []
    return []

def add_history(session_id: str, npc_id: str, role: str, text: str):
    current_time = time.time()
    session = session_manager.get_session(session_id)
    if session is None:
        raise ValueError("Session ID tidak valid")
    entry = {'role': role, 'parts': [text]}
    history_dict = session.get('history', {})
    history = history_dict.get(npc_id, [])
    history.append(entry)
    if len(history) > 10:
        history.pop(0)
    history_dict[npc_id] = history
    session_manager.set_session_data(session_id, 'history', history_dict)
    session_manager.set_session_data(session_id, 'last_access', current_time)