
import os
from pydantic import PrivateAttr
from typing import Any
from typing import Optional, List
from langchain.llms.base import LLM
import google.generativeai as genai

class GeminiLLM(LLM):
    model: str = os.getenv("GOOGLE_GEMINI_MODEL_NAME")
    temperature: float = 0
    _gemini: Any = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self._gemini = genai.GenerativeModel(self.model)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            response = self._gemini.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"[Gemini Error] {str(e)}"

    @property
    def _llm_type(self) -> str:
        return "google-gemini"