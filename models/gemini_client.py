"""
Shared Gemini client with retry logic and structured output support.
"""
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError, APIError, ClientError

load_dotenv()

# Free-tier friendly model fallback chain (August 2026)
# gemini-2.0-flash was shut down June 1, 2026
CANDIDATE_MODELS = [
    "gemini-3.5-flash",      # GA, behind gemini-flash-latest
    "gemini-2.5-flash",      # Still available
    "gemini-flash-latest",   # Alias to latest Flash
]


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise RuntimeError(
                "GEMINI_API_KEY not found in .env. "
                "Get a free key at https://aistudio.google.com/app/apikey"
            )
        self.client = genai.Client(api_key=api_key)

    def generate_structured(
        self,
        prompt: str,
        system_instruction: str,
        response_schema: dict,
        temperature: float = 0.4,
    ) -> dict:
        """
        Generate structured JSON using Gemini's JSON mode.
        Falls back through candidate models on 503 or 404 errors.
        """
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=response_schema,
            temperature=temperature,
        )

        last_error = None
        for model_name in CANDIDATE_MODELS:
            try:
                print(f"  [Gemini] Trying model: {model_name}...")
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config,
                )
                import json
                return json.loads(response.text)
            except (ServerError, APIError, ClientError) as e:
                last_error = e
                err_str = str(e)
                # Retry on 503 (busy) or 404 (model not found/shut down)
                if "503" in err_str or "404" in err_str or "NOT_FOUND" in err_str:
                    print(f"  [Gemini] {model_name} failed ({type(e).__name__}). Retrying next model...")
                    time.sleep(1.5)
                    continue
                raise e

        raise RuntimeError(f"All models exhausted. Last error: {last_error}")

    def generate_text(
        self,
        prompt: str,
        system_instruction: str = None,
        temperature: float = 0.7,
    ) -> str:
        """Generate plain text with fallback."""
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
        )

        last_error = None
        for model_name in CANDIDATE_MODELS:
            try:
                print(f"  [Gemini] Trying model: {model_name}...")
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config,
                )
                return response.text
            except (ServerError, APIError, ClientError) as e:
                last_error = e
                err_str = str(e)
                if "503" in err_str or "404" in err_str or "NOT_FOUND" in err_str:
                    print(f"  [Gemini] {model_name} failed ({type(e).__name__}). Retrying next model...")
                    time.sleep(1.5)
                    continue
                raise e

        raise RuntimeError(f"All models exhausted. Last error: {last_error}")