from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from dotenv import load_dotenv
load_dotenv()

def get_llm():

    llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash",
        temperature = 0.7,
    )

    return llm
