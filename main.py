import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError, APIError

load_dotenv()

def create_replit_workspace(project_title: str, language: str, index_html_content: str) -> dict:
    """
    Creates a live Replit workspace for film promotional pages and interactive storyboards.

    Args:
        project_title: Name of the Replit project or workspace.
        language: Workspace environment template (e.g., 'html', 'python').
        index_html_content: Raw HTML content for the landing page or storyboard viewer.
    """
    print(f"\n[TOOL CALLED] Provisioning Replit Workspace: '{project_title}'...")
    
    return {
        "status": "success",
        "workspace_url": f"https://replit.com/@demo/{project_title}",
        "live_site_url": f"https://{project_title}.replit.app",
        "files_written": ["index.html"]
    }

def run_agent():
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("[Notice] GEMINI_API_KEY missing in .env. Running local tool test:\n")
        res = create_replit_workspace(
            project_title="mars-thriller-teaser",
            language="html",
            index_html_content="<h1>Mars Thriller Landing Page</h1>"
        )
        print("Mock Tool Result:", res)
        return

    client = genai.Client(api_key=api_key)

    # Candidate models to try sequentially in case of 503 traffic spikes
    candidate_models = ["gemini-3.5-flash", "gemini-3.6-flash", "gemini-flash-latest"]
    
    prompt = (
        "Generate a landing page for a psychological thriller script called 'Echoes of Silence'. "
        "Use the create_replit_workspace tool to provision the workspace with full HTML."
    )

    for model_name in candidate_models:
        print(f"Attempting execution with model: '{model_name}'...")
        try:
            chat = client.chats.create(
                model=model_name,
                config=types.GenerateContentConfig(
                    tools=[create_replit_workspace],
                    temperature=0.2,
                )
            )

            response = chat.send_message(prompt)
            print("\nAgent Response:\n", response.text)
            break
        except (ServerError, APIError) as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"[Warning] {model_name} busy (503). Retrying with next model...\n")
                time.sleep(1)
            else:
                raise e

if __name__ == "__main__":
    run_agent()