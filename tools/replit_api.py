"""
Replit API integration.

CURRENT STATUS: Mock implementation for local development.
When Replit API credits are allocated, swap the body of deploy_project()
for real API calls using requests + your REPLIT_API_KEY.

Replit API docs: https://docs.replit.com/replit-workspace-api
"""
import os
from datetime import datetime


def deploy_project(project_title: str, html_content: str, css_content: str = "", js_content: str = "") -> dict:
    """
    Deploys a project to Replit.

    MOCK MODE: Saves files locally to output/ folder and returns a local file path.
    REAL MODE: Will create a Repl via Replit API, upload files, and deploy.
    """
    print(f"  [Replit] Deploying project: '{project_title}'...")

    # TODO: Replace this block with real Replit API integration
    # when API key/credits are available. Example real flow:
    #
    # import requests
    # headers = {"Authorization": f"Bearer {os.getenv('REPLIT_API_KEY')}"}
    # 1. Create Repl: POST https://api.replit.com/v0/repls
    # 2. Write files: POST to Replit filesystem API
    # 3. Deploy: POST to Replit deployments API
    # 4. Return live URL

    # MOCK: Save locally for preview
    safe_title = project_title.lower().replace(" ", "-").replace("_", "-")
    output_dir = f"output/{safe_title}"
    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    if css_content:
        with open(f"{output_dir}/style.css", "w", encoding="utf-8") as f:
            f.write(css_content)

    if js_content:
        with open(f"{output_dir}/script.js", "w", encoding="utf-8") as f:
            f.write(js_content)

    local_path = os.path.abspath(f"{output_dir}/index.html")

    print(f"  [Replit] ✅ MOCK deploy complete. Files saved to: {output_dir}/")
    print(f"  [Replit]    Open in browser: file://{local_path}")

    return {
        "status": "success",
        "mode": "MOCK",
        "local_path": local_path,
        "output_dir": output_dir,
        "workspace_url": f"https://replit.com/@demo/{safe_title}",  # placeholder
        "live_site_url": f"https://{safe_title}.replit.app",       # placeholder
        "files_written": ["index.html"] + (["style.css"] if css_content else []) + (["script.js"] if js_content else []),
        "deployed_at": datetime.now().isoformat(),
    }
