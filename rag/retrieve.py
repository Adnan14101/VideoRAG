from .vectorstore import load_vectorstore


_retriever = None

def get_retriever(video_name):
    global _retriever
    if _retriever is None:
        _retriever = load_vectorstore(video_name).as_retriever(
            search_type="similarity",
            search_kwargs={"k": 2}
        )
    return _retriever

def search(query: str):
    retriever = get_retriever()
    docs = retriever.invoke(query)
    
    # if not docs:
    #     return "No relevant documents were found in the knowledge base for this query."
    
    # context = "\n\n".join(
    #     f"Source: {doc.metadata.get('source','Unknown')}\n{doc.page_content}"
    #     for doc in docs
    # )

    # return context
    print("\nRelevant Chunks:\n")
    for i, doc in enumerate(docs):
        print(f"Chunk {i+1}")
        print(doc.page_content)
        print("------\n")
