import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

MOCK_LLM = os.getenv("MOCK_LLM", "false").lower() == "true"
PRICE_INPUT = float(os.getenv("PRICE_PER_1K_INPUT_TOKENS", "0.0"))
PRICE_OUTPUT = float(os.getenv("PRICE_PER_1K_OUTPUT_TOKENS", "0.0"))
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

usage_stats = {
    "latency_ms": 0,
    "cost_usd": 0.0,
    "model": MODEL
}

def reset_stats():
    usage_stats["latency_ms"] = 0
    usage_stats["cost_usd"] = 0.0

def call_llm(system_prompt: str, user_prompt: str, json_mode: bool = True) -> str:
    if MOCK_LLM:
        # Mock logic matching tests
        if "variations" in system_prompt.lower() or "enrich" in system_prompt.lower():
            return json.dumps({"query_variations": ["Ever since I installed a new app, swiping on my phone scrolls up and down instead of going left or right."]})
        
        elif "extract" in system_prompt.lower():
            return json.dumps({
                "goal": "Follow these steps to perform this Swipe Navigation Troubleshooting",
                "title": "Swipe navigation settings",
                "score": 0.93,
                "actions": [
                    {
                        "actionName": "Configure Navigation Bar Settings",
                        "description": "It will let you choose navigation type",
                        "category": "auto",
                        "stepGroups": [
                            {
                                "steps": [
                                    "Navigate to and open Settings.",
                                    "Tap on Display.",
                                    "Tap on Navigation bar.",
                                    "Select your preferred navigation type between Buttons and Swipe gestures."
                                ]
                            }
                        ]
                    }
                ]
            })
            
        elif "deeplink" in system_prompt.lower():
            return json.dumps({"selected_deeplink": "bixby://masked/act/display_navigation"})
            
        elif "repair" in system_prompt.lower():
            # In mock mode, if we reach repair, we just return the input since mock shouldn't fail
            return user_prompt
            
        return "{}"

    # Real LLM call
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("openai package not found. Run pip install openai")

    client = OpenAI(api_key=os.getenv("LLM_API_KEY"))
    
    start = time.time()
    response_format = {"type": "json_object"} if json_mode else {"type": "text"}
    
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format=response_format,
        temperature=0.0
    )
    elapsed = int((time.time() - start) * 1000)
    
    usage = completion.usage
    cost = (usage.prompt_tokens / 1000.0 * PRICE_INPUT) + (usage.completion_tokens / 1000.0 * PRICE_OUTPUT)
    
    usage_stats["latency_ms"] += elapsed
    usage_stats["cost_usd"] += cost
    
    return completion.choices[0].message.content
