from rag.memory import memory_store

def clear_memory(session_id):
    if session_id in memory_store:
        memory_store[session_id] = []
    print("MEMORY AFTER RESET:", memory_store.get(session_id))