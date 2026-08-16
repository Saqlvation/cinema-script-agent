"""
🎬 Agentic Cinema — The Full Pipeline

A deterministic 3-step agent that transforms film concepts into:
1. Structured screenplays (ScriptAgent / Director)
2. Visual storyboards with AI prompts (StoryboardAgent / Cinematographer)
3. Live pitch decks deployed via Replit (DeployAgent / Producer)

Run: python main.py
"""

import json
import os
from datetime import datetime

from agents.script_agent import ScriptAgent
from agents.storyboard_agent import StoryboardAgent
from agents.deploy_agent import DeployAgent


def save_json(data: dict, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  💾 Saved: {filepath}")


def save_html(html: str, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  💾 Saved: {filepath}")


def run_pipeline(concept: str) -> dict:
    """
    Runs the full 3-step agentic pipeline.
    Returns a dict with all artifacts and deployment info.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"run_{timestamp}"

    print("=" * 60)
    print("🎬 AGENTIC CINEMA — Production Pipeline")
    print("=" * 60)
    print(f"\n📝 Input Concept: {concept}\n")

    # ── STEP 1: DIRECTOR ──
    director = ScriptAgent()
    screenplay = director.develop(concept)

    save_json(screenplay, f"output/{run_id}/screenplay.json")

    # ── STEP 2: STORYBOARD ARTIST ──
    cinematographer = StoryboardAgent()
    storyboard = cinematographer.generate(screenplay)

    save_html(storyboard["html"], f"output/{run_id}/storyboard.html")

    # ── STEP 3: PRODUCER ──
    producer = DeployAgent()
    pitch_deck_html = producer.build_pitch_deck(screenplay, storyboard)

    deployment = producer.deploy(
        project_title=screenplay["title"],
        html_content=pitch_deck_html,
    )

    # Save pitch deck locally too
    save_html(pitch_deck_html, f"output/{run_id}/pitch_deck.html")

    # Summary
    print("\n" + "=" * 60)
    print("✅ PRODUCTION COMPLETE")
    print("=" * 60)
    print(f"\n📁 Run ID: {run_id}")
    print(f"🎬 Film: {screenplay['title']}")
    print(f"🎭 Characters: {len(screenplay['characters'])}")
    print(f"📜 Scenes: {len(screenplay['scenes'])}")
    print(f"🎨 Storyboard Panels: {len(storyboard['panels'])}")
    print(f"\n📂 Local Output: output/{run_id}/")
    print(f"   ├── screenplay.json")
    print(f"   ├── storyboard.html")
    print(f"   └── pitch_deck.html")

    if deployment.get("mode") == "MOCK":
        print(f"\n  Replit deploy is in MOCK mode.")
        print(f"   Local preview: file://{deployment['local_path']}")
        print(f"   When Replit API credits arrive, swap tools/replit_api.py")
    else:
        print(f"\n🚀 Live URL: {deployment['live_site_url']}")

    return {
        "run_id": run_id,
        "screenplay": screenplay,
        "storyboard": storyboard,
        "deployment": deployment,
    }


def main():
    print("\n Welcome to Agentic Cinema")
    print("Type your film concept below, or press Enter to use the demo concept.\n")

    demo_concept = (
        "A reclusive sound engineer who starts hearing fragments of conversations "
        "from 24 hours in the future, and must decide whether to prevent a tragedy "
        "she overhears or let fate play out."
    )

    user_input = input(f"Film concept: ").strip()
    concept = user_input if user_input else demo_concept

    if not user_input:
        print(f"\n(Using demo concept: {concept})\n")

    try:
        result = run_pipeline(concept)
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()
