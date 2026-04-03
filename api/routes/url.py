from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
import os
import uuid
from videoconverter.url_to_video import download_video
from api.services.videoservice import process_video
from api.utils.session_store import set_session_video
from api.utils.clear_memory import clear_memory

router = APIRouter()


class URLRequest(BaseModel):
    url: str


@router.post("/url")
def process_url(rq: URLRequest, request:Request, response:Response):

    session_id = request.cookies.get("session_id")

    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id)


    video_path = download_video(rq.url)

    video_name = os.path.basename(video_path).replace(".mp4", "")

    process_video(video_path, video_name)

      # ✅ bind video to session
    set_session_video(session_id, video_name)

    clear_memory(session_id)

    return {
        "message": "URL video processed successfully",
    }