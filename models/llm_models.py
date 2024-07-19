from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()


def get_model(api_choice):
    OPEN_API_KEY = os.environ["OPENAI_API_KEY"]
    if api_choice.lower() == "openai":
        return ChatOpenAI(model_name="gpt-4o", api_key=OPEN_API_KEY)
    elif api_choice.lower() == "gemini":
        return ChatGoogleGenerativeAI(model="gemini-pro")
    else:
        raise ValueError("Escolha inválida. Use 'openai' ou 'gemini'.")
