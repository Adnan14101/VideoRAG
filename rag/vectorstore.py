from langchain_chroma import Chroma
from .embedding import get_embeddings
import os

VECTOR_BASE_DIR = "rag/vector_db"
COLLECTION_NAME = "video_docs"


def get_vectorstore_dir(video_name):
    # folder per video
    return os.path.join(VECTOR_BASE_DIR, video_name)

def create_vectorstore(documents, video_name):
    persist_dir = get_vectorstore_dir(video_name)

    if os.path.exists(persist_dir):
        print(f"✅ Vectorstore for '{video_name}' already exists. Loading...")
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=get_embeddings()
        )

    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=COLLECTION_NAME
    )

    print("Vector DB created successfully")


# _vectorstore = None

# def load_vectorstore():
#     global _vectorstore
#     if _vectorstore is None:
#         _vectorstore = Chroma(
#             persist_directory=VECTOR_DIR,
#             embedding_function=get_embeddings(),
#             collection_name=COLLECTION_NAME
#         )
#     return _vectorstore

_vectorstore_cache = {}
def load_vectorstore(video_name):
    global _vectorstore_cache
    if video_name not in _vectorstore_cache:
        _vectorstore_cache[video_name] = Chroma(
            persist_directory=get_vectorstore_dir(video_name),
            embedding_function=get_embeddings(),
            collection_name=COLLECTION_NAME 
        )
    return _vectorstore_cache[video_name]