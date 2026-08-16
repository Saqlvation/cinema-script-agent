"""
Step 2: The Storyboard Artist
Takes a screenplay and generates visual prompts + an HTML storyboard grid.
"""
from models.gemini_client import GeminiClient


STORYBOARD_SCHEMA = {
    "type": "object",
    "properties": {
        "panels": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "scene_number": {"type": "integer"},
                    "shot_type": {"type": "string", "description": "e.g., Wide shot, Close-up, Over-the-shoulder, Aerial"},
                    "visual_prompt": {
                        "type": "string",
                        "description": "Detailed image-generation prompt (50-80 words). Describe lighting, camera angle, mood, color palette.",
                    },
                    "composition_notes": {"type": "string", "description": "Director's notes on framing and movement"},
                },
                "required": ["scene_number", "shot_type", "visual_prompt", "composition_notes"],
            },
        },
    },
    "required": ["panels"],
}

SYSTEM_PROMPT = """You are a master cinematographer and storyboard artist.
For each scene, you create a single iconic shot that captures the emotional essence of the moment.

Rules:
- Each visual prompt must be detailed enough for an AI image generator
- Vary shot types across the storyboard (don't use all close-ups)
- Include lighting direction, color palette, and lens choice
- Make prompts cinematic, not generic
"""


class StoryboardAgent:
    def __init__(self):
        self.client = GeminiClient()

    def generate(self, screenplay: dict) -> dict:
        """
        Takes a screenplay dict and returns panels with visual prompts.
        Also builds an HTML storyboard grid.
        """
        print("\n🎨 STEP 2: STORYBOARD ARTIST — Generating visual panels...")

        # Build a condensed scene list for the prompt
        scene_summaries = "\n".join([
            f"Scene {s['scene_number']} ({s['act']}): {s['setting']} — {s['description']}"
            for s in screenplay["scenes"]
        ])

        prompt = f"""Create a storyboard for the film "{screenplay['title']}".

GENRE: {screenplay['genre']}
TONE: {screenplay['tone']}

SCENES:
{scene_summaries}

For each scene, generate one iconic shot with a detailed visual prompt suitable for AI image generation."""

        result = self.client.generate_structured(
            prompt=prompt,
            system_instruction=SYSTEM_PROMPT,
            response_schema=STORYBOARD_SCHEMA,
            temperature=0.6,
        )

        # Build HTML storyboard
        html = self._build_html(screenplay, result["panels"])

        print(f"  ✅ Panels generated: {len(result['panels'])}")

        return {
            "panels": result["panels"],
            "html": html,
        }

    def _build_html(self, screenplay: dict, panels: list) -> str:
        """Builds a responsive HTML storyboard grid."""
        title = screenplay["title"]

        panels_html = ""
        for panel in panels:
            panels_html += f"""
            <div class="panel">
                <div class="panel-number">Scene {panel['scene_number']}</div>
                <div class="panel-shot">{panel['shot_type']}</div>
                <div class="panel-prompt">{panel['visual_prompt']}</div>
                <div class="panel-notes">🎬 {panel['composition_notes']}</div>
            </div>
            """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Storyboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: #0a0a0a; 
            color: #e0e0e0; 
            font-family: 'Segoe UI', system-ui, sans-serif;
            padding: 2rem;
        }}
        h1 {{ text-align: center; margin-bottom: 0.5rem; font-size: 2.5rem; letter-spacing: -1px; }}
        .subtitle {{ text-align: center; color: #888; margin-bottom: 2rem; }}
        .grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); 
            gap: 1.5rem; 
            max-width: 1400px; 
            margin: 0 auto;
        }}
        .panel {{ 
            background: #141414; 
            border: 1px solid #222; 
            border-radius: 12px; 
            padding: 1.5rem;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .panel:hover {{ transform: translateY(-4px); border-color: #444; }}
        .panel-number {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: #666; margin-bottom: 0.5rem; }}
        .panel-shot {{ font-weight: 700; color: #fff; margin-bottom: 0.75rem; font-size: 1.1rem; }}
        .panel-prompt {{ 
            font-style: italic; 
            color: #aaa; 
            line-height: 1.6; 
            margin-bottom: 1rem;
            font-size: 0.95rem;
        }}
        .panel-notes {{ font-size: 0.85rem; color: #777; border-top: 1px solid #222; padding-top: 0.75rem; }}
    </style>
</head>
<body>
    <h1>🎬 {title}</h1>
    <p class="subtitle">Visual Storyboard — Generated by Agentic Cinema</p>
    <div class="grid">
        {panels_html}
    </div>
</body>
</html>"""
