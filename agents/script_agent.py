"""
Step 1: The Director
Transforms a raw film concept into a structured screenplay.
"""
from models.gemini_client import GeminiClient


# JSON schema for structured screenplay output
SCREENPLAY_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Compelling film title"},
        "logline": {"type": "string", "description": "One-sentence hook (max 40 words)"},
        "genre": {"type": "string"},
        "tone": {"type": "string"},
        "characters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "role": {"type": "string", "description": "protagonist, antagonist, supporting"},
                    "description": {"type": "string", "description": "Physical and personality traits"},
                    "motivation": {"type": "string"},
                    "arc": {"type": "string", "description": "How they change by the end"},
                },
                "required": ["name", "role", "description", "motivation", "arc"],
            },
        },
        "scenes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "act": {"type": "string", "description": "Act 1, Act 2A, Act 2B, or Act 3"},
                    "scene_number": {"type": "integer"},
                    "setting": {"type": "string", "description": "Location and time of day"},
                    "description": {"type": "string", "description": "What happens in this scene (2-3 sentences)"},
                    "emotional_beat": {"type": "string", "description": "The feeling this scene should evoke"},
                    "key_dialogue": {"type": "string", "description": "One signature line from this scene"},
                },
                "required": ["act", "scene_number", "setting", "description", "emotional_beat", "key_dialogue"],
            },
        },
    },
    "required": ["title", "logline", "genre", "tone", "characters", "scenes"],
}

SYSTEM_PROMPT = """You are an acclaimed film director with 30 years of experience. 
Your job is to take a raw concept and develop it into a structured, production-ready screenplay treatment.

Rules:
- Create 6-8 distinct scenes across a 3-act structure
- Each character must have a clear arc
- Settings should be cinematic and specific
- Emotional beats must escalate toward a climax
- Write in English
"""


class ScriptAgent:
    def __init__(self):
        self.client = GeminiClient()

    def develop(self, concept: str) -> dict:
        """
        Takes a raw film concept and returns a structured screenplay dict.
        """
        print("\n🎬 STEP 1: DIRECTOR — Developing screenplay...")

        prompt = f"""Develop the following film concept into a full screenplay treatment:

CONCEPT: {concept}

Output a complete structured screenplay with title, logline, genre, tone, characters, and scenes."""

        result = self.client.generate_structured(
            prompt=prompt,
            system_instruction=SYSTEM_PROMPT,
            response_schema=SCREENPLAY_SCHEMA,
            temperature=0.5,
        )

        print(f"  ✅ Title: {result['title']}")
        print(f"  ✅ Logline: {result['logline']}")
        print(f"  ✅ Characters: {len(result['characters'])}")
        print(f"  ✅ Scenes: {len(result['scenes'])}")

        return result
