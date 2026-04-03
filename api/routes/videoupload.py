from fastapi import APIRouter, UploadFile, File, Request, Response
import os
import shutil
import uuid
from api.services.videoservice import process_video
from api.utils.session_store import set_session_video
from api.utils.clear_memory import clear_memory

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/uploads")
async def upload_video(request:Request,response:Response,file: UploadFile = File(...)):

    # ✅ get/create session
    session_id = request.cookies.get("session_id")

    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    video_name = file.filename.replace(".mp4", "")

    process_video(file_path, video_name)

    
    # ✅ bind video to session
    set_session_video(session_id, video_name)

    # 🔥 reset memory
    clear_memory(session_id)

    return {
        "message": "Video processed successfully",
    }