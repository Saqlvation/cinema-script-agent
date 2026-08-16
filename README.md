# cinema-script-agent
An autonomous multi-step agent pipeline built for the **Agentic Cinema Hackathon**. Powered by Google Gemini and Replit, this agent transforms film concepts into structured screenplays, storyboard prompts, and live interactive promotional landing pages

### features
1. **Script Analysis & Development:** Analyzes high-concept ideas to generate loglines, character profiles, and scene breakdowns.
2. **Visual Storyboard Engine:** Generates cinematic visual prompts for key scenes.
3. **Replit Web Deployment:** Automatically provisions and deploys interactive script readers and pitch decks to live Replit environments.

### Tech stack
* **LLM Engine:** Google Gemini (`google-genai` SDK)
* **Deployment Integration:** Replit API
* **Environment:** Python 3.12+


### Quickstart
1. **Clone the repository:**
```bash
   git clone https://github.com/Saqlvation/cinema-script-agent.git
   cd cinema-script-agent
``` 

2. **Set up virtual environment:**
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
```
3. **Install dependencies:**
```bash
pip install google-genai requests python-dotenv
```

4. **Configure environment variables:**
    Create a .env file in the root directory:
```bash
    GEMINI_API_KEY=your_gemini_api_key
    REPLIT_API_KEY=your_replit_api_key
```

5. **Run the agent:**
```bash
    python main.py
```


