# 🎥 VideoRAG

A Retrieval Augmented Generation (RAG) system that allows you to chat with your videos. Upload a video or provide a URL, and ask questions about its content using natural language.

## 🌟 Features

- **Video Processing**: Extract audio and transcribe videos using OpenAI Whisper
- **Vector Search**: Store and search transcript embeddings using ChromaDB
- **RAG Chat**: Ask questions about video content with context-aware responses
- **Multi-language Support**: Understands English, Hindi, Hinglish, and mixed languages
- **Multiple Interfaces**: 
  - CLI (Command Line Interface)
  - Streamlit Web App
  - FastAPI REST API
  - Static HTML Frontend

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Video Input   │────▶│  Video Processor │────▶│   Transcript    │
│ (Upload/URL)    │     │ (Whisper)        │     │   (Text)        │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                           │
                                                           ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Query   │────▶│  RAG Pipeline     │◀────│  Vector Store   │
│                │     │ (LangChain+Gemini)│     │   (ChromaDB)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## 📁 Project Structure

```
videorag/
├── main.py                 # CLI entry point
├── streamlit_app.py        # Streamlit web interface
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project metadata
├── .env                    # Environment variables
│
├── api/                    # FastAPI backend
│   ├── main.py            # API server
│   ├── routes/
│   │   ├── chat.py       # Chat endpoint
│   │   ├── health.py     # Health check
│   │   ├── url.py        # URL video download
│   │   └── videoupload.py # Video upload
│   └── services/
│       └── videoservice.py
│
├── rag/                    # RAG components
│   ├── llm.py             # LLM integration (Gemini)
│   ├── vectorstore.py     # ChromaDB vector store
│   ├── retrieve.py        # Retrieval logic
│   ├── splitter.py        # Text chunking
│   ├── memory.py          # Chat memory
│   ├── embedding.py       # Embeddings
│   └── cleaner.py         # Text cleaning
│
├── videoconverter/         # Video processing
│   ├── video_to_text.py   # Audio extraction & transcription
│   ├── url_to_video.py    # URL video download
│   └── transcript.txt     # Sample transcript
│
├── static/                 # Static frontend
│   └── index.html
│
├── uploads/                # Uploaded videos
├── utils/                  # Utilities
└── rag/vector_db/          # Vector database storage
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- FFmpeg (for audio extraction)
- Google API Key (for Gemini LLM)

### Installation

1. **Clone the repository**

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Install FFmpeg** (required for audio extraction)
   - Windows: Download from https://ffmpeg.org/download.html
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

## 💻 Usage

### Option 1: CLI Interface

Run the command-line interface:
```bash
python main.py
```

Enter a video file path or URL when prompted:
```
🎥 Video RAG CLI

Enter video path OR URL: https://example.com/video.mp4
```

Then ask questions about the video content.

### Option 2: Streamlit Web App

Start the Streamlit interface:
```bash
streamlit run streamlit_app.py
```

Open your browser at `http://localhost:8501`

### Option 3: FastAPI Server

Start the API server:
```bash
python -m uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

#### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve static frontend |
| `/api/v1/upload` | POST | Upload a video file |
| `/api/v1/url` | POST | Download video from URL |
| `/api/v1/chat` | POST | Chat with video |
| `/api/v1/health` | GET | Health check |

## 🔧 How It Works

### Video Processing Pipeline

1. **Video Input**: Accept video file (mp4, mov, mkv) or URL
2. **Audio Extraction**: Extract audio track using FFmpeg
3. **Transcription**: Convert audio to text using OpenAI Whisper
4. **Text Splitting**: Chunk transcript into manageable segments
5. **Embedding**: Create vector embeddings using LangChain
6. **Storage**: Store embeddings in ChromaDB vector database

### RAG Query Pipeline

1. **Query Input**: User asks a question
2. **History Integration**: Combine with previous chat history
3. **Retrieval**: Find relevant transcript segments using similarity search
4. **LLM Generation**: Generate answer using Gemini with retrieved context
5. **Memory Update**: Store conversation for continuity

## 📝 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google API key for Gemini LLM | Yes |

### Supported Video Formats

- MP4
- MOV
- MKV
- AVI

## 🛠️ Tech Stack

- **Video Processing**: FFmpeg, OpenAI Whisper
- **Vector Database**: ChromaDB
- **LLM**: Google Gemini (via LangChain)
- **Web Framework**: FastAPI, Streamlit
- **Frontend**: HTML, CSS, JavaScript
- **Embeddings**: HuggingFace

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
