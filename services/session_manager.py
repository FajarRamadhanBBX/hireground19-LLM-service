import uuid
import time

# Penyimpanan sesi dalam memori (private)
_sessions = {"1": {'last_access': 0.0, 'history': []}}
# Struktur: {session_id: 'str', {'last_access': 'float', 'history': 'list'}}

def generate_session_id():
    session_id = str(uuid.uuid4())
    _sessions[session_id] = {}
    return {"session_id": session_id}

def is_valid_session(session_id: str):
    return session_id in _sessions

def get_session(session_id: str):
    return _sessions.get(session_id)

def set_session_data(session_id: str, key: str, value):
    if session_id in _sessions:
        _sessions[session_id][key] = value
        return True
    return False

def get_session_data(session_id: str, key: str):
    if session_id in _sessions:
        return _sessions[session_id].get(key)
    return None

def get_all_sessions():
    return _sessions

def delete_session(session_id: str):
    if session_id in _sessions:
        _sessions.pop(session_id)
        print(f"Session {session_id} terhapus.")
        return True
    return False

def cleanup_expired_sessions(timeout_seconds=1800):
    now = time.time()
    expired = []
    for session_id, data in list(_sessions.items()):
        last_access = data.get('last_access')
        if last_access is not None and now - last_access > timeout_seconds:
            expired.append(session_id)
    for session_id in expired:
        _sessions.pop(session_id)
        print(f"Session {session_id} expired and deleted.")
    return expired