from videoconverter.video_to_text import extract_audio_from_video,transcribe_audio
from rag.splitter import splitter
from rag.retrieve import search
from rag.vectorstore import create_vectorstore
from rag.llm import ask_rag
import os
from rag.vectorstore import get_vectorstore_dir, load_vectorstore
from videoconverter.url_to_video import download_video

def main():

    # # video_path = "videoplayback.mp4"
    # print("🎥 Video RAG CLI\n")

    # video_path = input("Enter path to video: ").strip()
    # if not os.path.exists(video_path):
    #     print("❌ Video file not found!")
    #     return

    # video_name = os.path.basename(video_path).replace(".mp4", "")
    # vectorstore_dir = get_vectorstore_dir(video_name)

    # # Step 1: Check if vectorstore exists
    # if os.path.exists(os.path.join(vectorstore_dir, "chroma.sqlite3")):
    #     print(f"✅ Vectorstore for '{video_name}' already exists. Skipping transcription & splitting.")
    # else:
    #      # Extract audio
    #     audio_path = extract_audio_from_video(video_path)
    
    #     # Transcribe
    #     transcript = transcribe_audio(audio_path)
    
    #     #Build RAG
    #     splits = splitter(transcript)
    #     create_vectorstore(splits,video_name)
    
    # # # Example query
    # # question = "What is the main topic discussed in the video?"
    # # answer = search(question)
    # # print("Answer:", answer)
    # while True:
    #     try:
    #         query = input("🧑 You: ").strip()

    #         if query.lower() in ["exit", "quit"]:
    #             print("\n👋 Exiting... Bye!")
    #             break

    #         if not query:
    #             continue

    #         print("\n🤖 Thinking...\n")

    #         answer = ask_rag(query,video_name)

    #         print(f"🤖 AI:\n{answer}\n")

    #     except KeyboardInterrupt:
    #         print("\n\n👋 Interrupted. Exiting...")
    #         break

    #     except Exception as e:
    #         print(f"\n❌ Error: {e}\n")

    print("🎥 Video RAG CLI\n")

    user_input = input("Enter video path OR URL: ").strip()

    # 🔥 Detect URL vs file
    if user_input.startswith("http"):
        print("🌐 Downloading video from URL...")
        video_path = download_video(user_input)
    else:
        video_path = user_input

    if not os.path.exists(video_path):
        print("❌ Video file not found!")
        return

    video_name = os.path.basename(video_path).replace(".mp4", "")
    vectorstore_dir = get_vectorstore_dir(video_name)

    db_file = os.path.join(vectorstore_dir, "chroma.sqlite3")

    # ✅ Check DB
    if os.path.exists(db_file):
        print(f"✅ Vectorstore for '{video_name}' already exists.")
    else:
        print("⚙️ Processing video...")

        audio_path = extract_audio_from_video(video_path)
        transcript = transcribe_audio(audio_path)
        splits = splitter(transcript)

        print("Splits:", len(splits))

        create_vectorstore(splits, video_name)

    # 💬 Chat loop
    while True:
        query = input("🧑 You: ").strip()

        if query.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        if not query:
            continue

        print("\n🤖 Thinking...\n")

        answer = ask_rag(query, video_name,session_id="user123")
        print(f"🤖 AI:\n{answer}\n")


if __name__ == "__main__":
    main()
