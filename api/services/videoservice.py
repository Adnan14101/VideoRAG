import os

from videoconverter.video_to_text import extract_audio_from_video, transcribe_audio
from rag.splitter import splitter
from rag.vectorstore import create_vectorstore, get_vectorstore_dir


def process_video(video_path: str, video_name: str):

    vectorstore_dir = get_vectorstore_dir(video_name)
    db_file = os.path.join(vectorstore_dir, "chroma.sqlite3")

    if os.path.exists(db_file):
        print(f"✅ Vectorstore exists for {video_name}")
        return

    print("⚙️ Processing video...")

    audio_path = extract_audio_from_video(video_path)
    transcript = transcribe_audio(audio_path)
    splits = splitter(transcript)

    print("Splits:", len(splits))

    create_vectorstore(splits, video_name)