import os
import requests
from typing import Type, ClassVar, Optional
from pydantic import BaseModel
from langchain.tools import BaseTool

class InputSchema(BaseModel):
    query: str

class GoogleSearchTool(BaseTool):
    name: ClassVar[str] = "Google Search"
    description: ClassVar[str] = "Use BrightData SERP API to search Google."
    args_schema: ClassVar[Type[BaseModel]] = InputSchema

    def _run(self, query: str) -> Optional[str]:
        api_key = os.getenv("BRIGHTDATA_SERP_API_KEY")
        if not api_key:
            return "[ERROR] Bright Data SERP API key not found."

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "gl": "us",
            "hl": "en",
            "num": 3
        }

        try:
            res = requests.post("https://serp-api.brightdata.com/search", headers=headers, json=payload, timeout=15)
            res.raise_for_status()
            data = res.json()

            results = data.get("organic", [])
            if not results:
                return "No results found."

            output = []
            for r in results:
                title = r.get("title", "No title")
                link = r.get("link", "No link")
                snippet = r.get("snippet", "No snippet")
                output.append(f"{title}\n{link}\n{snippet}\n")

            return "\n".join(output)

        except Exception as e:
            return f"[GoogleSearchTool Error] {str(e)}"

    def _arun(self, query: str):
        raise NotImplementedError("Async version not implemented.")
