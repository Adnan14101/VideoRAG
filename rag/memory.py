memory_store = {}

def get_memory(session_id):
    if session_id not in memory_store:
        memory_store[session_id] = []
    return memory_store[session_id]

def update_memory(session_id, role, content):
    memory_store[session_id].append({
        "role": role,
        "content": content
    })

    # 🔥 keep only last 6 messages (short-term memory)
    memory_store[session_id] = memory_store[session_id][-6:]

from langchain.messages import HumanMessage, SystemMessage, AIMessage

def build_chat_history(session_id):
    history = get_memory(session_id)

    messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))

    return messages

def rewrite_query(query, chat_history, llm):
    messages = [
        SystemMessage(content="Rewrite the query into a clear standalone question."),
        *chat_history,
        HumanMessage(content=query)
    ]
    return llm.invoke(messages).content