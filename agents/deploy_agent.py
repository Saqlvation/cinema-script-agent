"""
Step 3: The Producer
Assembles the final pitch deck and deploys it.
"""
from tools.replit_api import deploy_project


class DeployAgent:
    def __init__(self):
        pass

    def build_pitch_deck(self, screenplay: dict, storyboard: dict) -> str:
        """
        Renders a complete cinematic pitch deck HTML page.
        """
        print("\n🚀 STEP 3: PRODUCER — Building pitch deck...")

        title = screenplay["title"]
        logline = screenplay["logline"]
        genre = screenplay["genre"]
        tone = screenplay["tone"]

        # Characters section
        chars_html = ""
        for char in screenplay["characters"]:
            chars_html += f"""
            <div class="character-card">
                <h3>{char['name']} <span class="role">{char['role']}</span></h3>
                <p class="char-desc">{char['description']}</p>
                <p class="char-motivation"><strong>Motivation:</strong> {char['motivation']}</p>
                <p class="char-arc"><strong>Arc:</strong> {char['arc']}</p>
            </div>
            """

        # Scenes timeline
        scenes_html = ""
        for scene in screenplay["scenes"]:
            scenes_html += f"""
            <div class="scene-item">
                <div class="scene-meta">
                    <span class="act-badge">{scene['act']}</span>
                    <span class="scene-num">Scene {scene['scene_number']}</span>
                </div>
                <h4>{scene['setting']}</h4>
                <p>{scene['description']}</p>
                <p class="emotional-beat">💫 {scene['emotional_beat']}</p>
                <p class="dialogue">“{scene['key_dialogue']}”</p>
            </div>
            """

        # Storyboard panels
        panels_html = ""
        for panel in storyboard["panels"]:
            panels_html += f"""
            <div class="sb-panel">
                <div class="sb-header">
                    <span class="sb-scene">Scene {panel['scene_number']}</span>
                    <span class="sb-shot">{panel['shot_type']}</span>
                </div>
                <p class="sb-prompt">{panel['visual_prompt']}</p>
                <p class="sb-notes">🎬 {panel['composition_notes']}</p>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Pitch Deck</title>
    <style>
        :root {{
            --bg: #0a0a0a;
            --surface: #111111;
            --surface-hover: #1a1a1a;
            --border: #222222;
            --text: #e8e8e8;
            --text-secondary: #888888;
            --accent: #e50914;
            --accent-glow: rgba(229, 9, 20, 0.3);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            line-height: 1.6;
        }}
        .hero {{
            min-height: 60vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(180deg, rgba(229,9,20,0.1) 0%, var(--bg) 100%);
            border-bottom: 1px solid var(--border);
        }}
        .hero h1 {{
            font-size: clamp(2.5rem, 6vw, 5rem);
            font-weight: 800;
            letter-spacing: -2px;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #fff 0%, #aaa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero .meta {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .badge {{
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 0.35rem 0.9rem;
            border-radius: 100px;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .logline {{
            max-width: 700px;
            font-size: 1.25rem;
            color: var(--text-secondary);
            font-style: italic;
            line-height: 1.5;
        }}
        .section {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 4rem 2rem;
            border-bottom: 1px solid var(--border);
        }}
        .section h2 {{
            font-size: 1.75rem;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        .characters-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }}
        .character-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s;
        }}
        .character-card:hover {{
            transform: translateY(-3px);
            border-color: var(--accent);
            box-shadow: 0 8px 24px var(--accent-glow);
        }}
        .character-card h3 {{
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .role {{
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            background: var(--accent);
            color: white;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-weight: 600;
        }}
        .char-desc {{ color: var(--text-secondary); margin-bottom: 0.75rem; font-size: 0.95rem; }}
        .char-motivation, .char-arc {{ font-size: 0.9rem; margin-bottom: 0.4rem; }}
        .char-arc {{ color: #aaa; }}

        .timeline {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        .scene-item {{
            background: var(--surface);
            border-left: 3px solid var(--accent);
            padding: 1.5rem;
            border-radius: 0 12px 12px 0;
        }}
        .scene-meta {{
            display: flex;
            gap: 0.75rem;
            margin-bottom: 0.75rem;
            align-items: center;
        }}
        .act-badge {{
            background: var(--accent);
            color: white;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            letter-spacing: 1px;
        }}
        .scene-num {{ color: var(--text-secondary); font-size: 0.85rem; }}
        .scene-item h4 {{ font-size: 1.1rem; margin-bottom: 0.5rem; }}
        .emotional-beat {{ color: #c9a227; font-size: 0.9rem; margin-top: 0.75rem; font-style: italic; }}
        .dialogue {{
            margin-top: 0.5rem;
            font-family: Georgia, serif;
            color: #ccc;
            border-left: 2px solid #444;
            padding-left: 1rem;
            font-size: 0.95rem;
        }}

        .storyboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        .sb-panel {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
        }}
        .sb-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.75rem;
            align-items: center;
        }}
        .sb-scene {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: #666; }}
        .sb-shot {{ font-weight: 700; color: var(--accent); }}
        .sb-prompt {{ font-style: italic; color: #aaa; line-height: 1.5; margin-bottom: 1rem; font-size: 0.95rem; }}
        .sb-notes {{ font-size: 0.85rem; color: #777; border-top: 1px solid var(--border); padding-top: 0.75rem; }}

        .footer {{
            text-align: center;
            padding: 3rem 2rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        .footer a {{ color: var(--accent); text-decoration: none; }}

        @media (max-width: 600px) {{
            .hero {{ padding: 2rem 1rem; }}
            .section {{ padding: 2rem 1rem; }}
        }}
    </style>
</head>
<body>
    <header class="hero">
        <h1>{title}</h1>
        <div class="meta">
            <span class="badge">{genre}</span>
            <span class="badge">{tone}</span>
        </div>
        <p class="logline">{logline}</p>
    </header>

    <section class="section">
        <h2>🎭 Characters</h2>
        <div class="characters-grid">
            {chars_html}
        </div>
    </section>

    <section class="section">
        <h2>📜 Screenplay</h2>
        <div class="timeline">
            {scenes_html}
        </div>
    </section>

    <section class="section">
        <h2>🎨 Storyboard</h2>
        <div class="storyboard-grid">
            {panels_html}
        </div>
    </section>

    <footer class="footer">
        <p>Generated by <strong>Agentic Cinema</strong> — Gemini × Replit</p>
        <p style="margin-top: 0.5rem; font-size: 0.8rem;">Built for the Agentic Cinema Hackathon</p>
    </footer>
</body>
</html>"""

        return html

    def deploy(self, project_title: str, html_content: str) -> dict:
        """
        Deploys the pitch deck. Currently uses mock Replit deploy.
        """
        result = deploy_project(
            project_title=project_title,
            html_content=html_content,
        )
        return result
