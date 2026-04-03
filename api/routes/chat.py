from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
import uuid
from rag.llm import ask_rag
from api.utils.session_store import get_session_video

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
def chat(rq: ChatRequest,request:Request,response:Response):

    session_id = request.cookies.get("session_id")

    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id)

        # ✅ get video automatically
    video_name = get_session_video(session_id)

    if not video_name:
        return {
            "answer": "No video found for this session. Please upload a video first."
        }

    query = rq.query.lower().strip()

    if query in ["hello","hi","hey"]:
        return {"answer": "Hello! How can I help you?"}
    elif query in ["thank you","thanks"]:
        return {"answer": "You're Welcome!"}
    # if any(word in query for word in ["hello", "hi", "hey"]):
    #     return {"answer": "Hello! How can I help you?"}
    # elif any(word in query for word in ["thank", "thanks"]):
    #     return {"answer": "You're welcome!"}
   
    answer = ask_rag(rq.query, video_name, session_id)

    return {
        "answer": answer
    }