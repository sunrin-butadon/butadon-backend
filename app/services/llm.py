from openai import OpenAI
from app.core.config import settings

class LLM():
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)