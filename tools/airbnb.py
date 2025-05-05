import os
import requests
from typing import Type, ClassVar
from pydantic import BaseModel
from langchain.tools import BaseTool

class AirbnbInputSchema(BaseModel):
    location: str

class AirbnbTool(BaseTool):
    name: ClassVar[str] = "Airbnb Search"
    description: ClassVar[str] = "Scrape Airbnb listings using Bright Data Web Unlocker."
    args_schema: ClassVar[Type[BaseModel]] = AirbnbInputSchema

    def _run(self, location: str) -> str:
        token = os.getenv("BRIGHTDATA_BEARER_TOKEN")
        if not token:
            return "[ERROR] Bright Data Web Unlocker token missing."

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "url": f"https://www.airbnb.com/s/{location}/homes",
            "zone": "web_unlocker1",
            "render": True
        }

        try:
            response = requests.post(
                "https://api.brightdata.com/dca/trigger?collector=smart",
                headers=headers,
                json=payload,
                timeout=20
            )
            response.raise_for_status()
            job = response.json()
            job_id = job.get("collection_id")

            if not job_id:
                return "[ERROR] Failed to trigger collection: missing job ID."

            # Polling logic should be added here for real use cases
            return f"Airbnb listings fetch triggered for '{location}'. Job ID: {job_id}"

        except requests.RequestException as e:
            return f"[AirbnbTool Error] Request failed: {str(e)}"
        except Exception as e:
            return f"[AirbnbTool Error] Unexpected error: {str(e)}"

    def _arun(self, location: str):
        raise NotImplementedError("Async version not implemented.")
