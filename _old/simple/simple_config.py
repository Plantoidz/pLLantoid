from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    OPENAI_API_KEY = os.environ.get("OPENAI")
    ELEVEN_LABS_API_KEY = os.environ.get("ELEVEN")
    MODEL_ID = "text-davinci-003"
