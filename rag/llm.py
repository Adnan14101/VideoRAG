from utils.llm import get_llm
from .vectorstore import load_vectorstore
from .retrieve import get_retriever
from langchain.messages import HumanMessage, SystemMessage
from .memory import build_chat_history, rewrite_query, update_memory,memory_store

def ask_rag(query:str,video_name:str,session_id):

    retriever = get_retriever(video_name)
    llm = get_llm()

    # ✅ memory
    chat_history = build_chat_history(session_id)
    print("DEBUG CHAT HISTORY:", chat_history)

    # ✅ rewrite query
    query = rewrite_query(query, chat_history, llm)

    docs_with_scores = retriever.vectorstore.similarity_search_with_score(query, k=6)

    docs = []
    seen = set()

    for doc, score in docs_with_scores:
        if doc.page_content not in seen:
            docs.append(doc)
            seen.add(doc.page_content)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )
    print("\nDEBUG: Retrieved Docs ->", len(docs))
    print("DEBUG: Context ->", context[:500])

    # system_message = SystemMessage(
    #     content="You are an AI assistant that answers questions ONLY from a provided video transcript."
    # )
    
    messages = [
        SystemMessage(content="""
You are an AI assistant that answers questions ONLY from a provided video transcript.

Rules:
1. Understand queries in any language (English, Hindi, Hinglish, or mixed).
2. Always answer in the SAME language as the user’s question.
3. If the answer is not present in the provided context, say:
   "The answer is not available in the video."
4. Maintain conversation continuity using previous messages.
5. Do not use outside knowledge. Answer strictly from the given context.
6. Keep answers clear, simple, and relevant.
7. Treat Hinglish (Hindi written in English letters) as Hindi.

Examples:
- If user asks in Hindi → answer in Hindi
- If user asks in Hinglish → answer in Hinglish
- If user mixes languages → respond similarly
"""),
        *chat_history,
         HumanMessage(content=f"""
Context:
{context}

Question:
{query}
""")]

#     human_message = HumanMessage(
#         content=f"""
# Context:
# {context}

# Question:
# {query}

# Answer directly using only the context.
# If the answer is not in the context, say:
# "I couldn't find that information in the video."
# """
#     )

    response = llm.invoke(messages)
     # ✅ update memory
    update_memory(session_id, "user", query)
    update_memory(session_id, "ai", response.content)
    print("DEBUG MEMORY:", memory_store[session_id])

    return response.content