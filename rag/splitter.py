from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def splitter(transcript):

    doc = Document(page_content=transcript)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    splits = text_splitter.split_documents([doc])

    if len(splits) == 0:
        raise ValueError("No chunks created")
    
    print("Total chunks:", len(splits))
    # print(splits)

    return splits
