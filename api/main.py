from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import videoupload, url, chat, health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Video RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videoupload.router)
app.include_router(url.router)
app.include_router(chat.router)
app.include_router(health.router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at root
@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")