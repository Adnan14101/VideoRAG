# # app.py
# import streamlit as st
# import os
# from  videoconverter.url_to_video import download_video
# from videoconverter.video_to_text import extract_audio_from_video, transcribe_audio
# from rag.splitter import splitter
# from rag.vectorstore import create_vectorstore, get_vectorstore_dir
# from rag.llm import ask_rag

# st.set_page_config(page_title="VideoRAG Chat", layout="wide")
# st.title("🎥 VideoRAG - Chat with Your Video")

# # Session state for video processing
# if "video_name" not in st.session_state:
#     st.session_state.video_name = None
# if "vectorstore_ready" not in st.session_state:
#     st.session_state.vectorstore_ready = False
# if "history" not in st.session_state:
#     st.session_state.history = []

# # Upload video or enter URL
# video_input = st.file_uploader("Upload a video", type=["mp4", "mov", "mkv"])
# video_url = st.text_input("Or enter a video URL:")

# video_path = None
# if video_input:
#     video_path = os.path.join("uploads", video_input.name)
#     os.makedirs("uploads", exist_ok=True)
#     with open(video_path, "wb") as f:
#         f.write(video_input.getbuffer())
# elif video_url:
#     if st.button("Download Video"):
#         st.info("🌐 Downloading video...")
#         video_path = download_video(video_url)
#         st.success(f"Downloaded video: {video_path}")

# # Process video
# if video_path:
#     video_name = os.path.basename(video_path).replace(".mp4", "")
#     st.session_state.video_name = video_name
#     vectorstore_dir = get_vectorstore_dir(video_name)
#     db_file = os.path.join(vectorstore_dir, "chroma.sqlite3")

#     if os.path.exists(db_file):
#         st.session_state.vectorstore_ready = True
#         st.success(f"✅ Vectorstore for '{video_name}' already exists.")
#     else:
#         if st.button("Process Video"):
#             with st.spinner("⚙️ Extracting audio, transcribing, and building vectorstore..."):
#                 audio_path = extract_audio_from_video(video_path)
#                 transcript = transcribe_audio(audio_path)
#                 splits = splitter(transcript)
#                 create_vectorstore(splits, video_name)
#                 st.session_state.vectorstore_ready = True
#                 st.success("✅ Video processed and vectorstore created!")

# # Chat interface
# if st.session_state.vectorstore_ready:
#     st.subheader("Ask questions about your video")
#     user_question = st.text_input("Your question:")

#     if st.button("Ask") and user_question:
#         st.session_state.history.append(("You", user_question))
#         with st.spinner("🤖 Thinking..."):
#             answer = ask_rag(user_question, st.session_state.video_name)
#             st.session_state.history.append(("VideoRAG", answer))

#     # Display chat history
#     if st.session_state.history:
#         for speaker, msg in st.session_state.history:
#             if speaker == "You":
#                 st.markdown(f"**You:** {msg}")
#             else:
#                 st.markdown(f"**VideoRAG:** {msg}")

# app.py
import streamlit as st
import os
from videoconverter.url_to_video import download_video
from videoconverter.video_to_text import extract_audio_from_video, transcribe_audio
from rag.splitter import splitter
from rag.vectorstore import create_vectorstore, get_vectorstore_dir
from rag.llm import ask_rag

st.set_page_config(page_title="VideoRAG Chat", layout="wide")

# ---------------- SESSION STATE ----------------
if "video_name" not in st.session_state:
    st.session_state.video_name = None
if "vectorstore_ready" not in st.session_state:
    st.session_state.vectorstore_ready = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "video_path" not in st.session_state:
    st.session_state.video_path = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🎥 VideoRAG")

    st.markdown("### Upload Video")
    uploaded_file = st.file_uploader("Choose file", type=["mp4", "mov", "mkv"])

    st.markdown("### Or paste URL")
    video_url = st.text_input("Video URL")

    if uploaded_file:
        os.makedirs("uploads", exist_ok=True)
        video_path = os.path.join("uploads", uploaded_file.name)

        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state.video_path = video_path
        st.success("✅ Video uploaded")

    if video_url:
        if st.button("Download Video"):
            with st.spinner("Downloading..."):
                video_path = download_video(video_url)
                st.session_state.video_path = video_path
                st.success("✅ Downloaded")

    # Process button
    if st.session_state.video_path:
        if st.button("⚙️ Process Video"):
            video_path = st.session_state.video_path
            video_name = os.path.basename(video_path).replace(".mp4", "")
            st.session_state.video_name = video_name

            vectorstore_dir = get_vectorstore_dir(video_name)
            db_file = os.path.join(vectorstore_dir, "chroma.sqlite3")

            if os.path.exists(db_file):
                st.session_state.vectorstore_ready = True
                st.success("✅ Already processed")
            else:
                with st.spinner("Processing video..."):
                    audio_path = extract_audio_from_video(video_path)
                    transcript = transcribe_audio(audio_path)
                    splits = splitter(transcript)
                    create_vectorstore(splits, video_name)

                    st.session_state.vectorstore_ready = True
                    st.success("✅ Processing complete")

    st.markdown("---")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

# ---------------- MAIN CHAT UI ----------------

st.title("💬 Chat with your Video")

# Show video preview
if st.session_state.video_path:
    st.video(st.session_state.video_path)

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input (ChatGPT style)
if st.session_state.vectorstore_ready:
    prompt = st.chat_input("Ask something about the video...")

    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask_rag(prompt, st.session_state.video_name)
                st.markdown(response)

        # Save response
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("👈 Upload and process a video to start chatting.")