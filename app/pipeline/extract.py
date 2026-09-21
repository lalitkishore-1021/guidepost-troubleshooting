import json
from app.llm import call_llm

def extract_plan(siis_text: str):
    system = """Extract troubleshooting plan from the text. Output JSON exactly matching:
    {
      "goal": "Follow these steps to perform this <Topic> Troubleshooting",
      "title": "2 to 3 words, sentence case",
      "score": 0.9,
      "actions": [
        {
           "actionName": "Title Case",
           "description": "It will ... (exactly 5 to 7 words starting with 'It will')",
           "category": "auto|manual|critical",
           "stepGroups": [{"steps": ["step 1", "step 2"]}]
        }
      ]
    }
    Rules:
    - Do NOT include URLs or HTTP links.
    - Extract ONLY from the source text.
    - Category 'critical' is for factory reset, restart, safe mode, etc.
    """
    res = call_llm(system, siis_text, json_mode=True)
    try:
        return json.loads(res)
    except:
        return None
