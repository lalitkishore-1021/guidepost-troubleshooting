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
        u = user_prompt.lower()
        # Mock logic matching tests
        if "variations" in system_prompt.lower() or "enrich" in system_prompt.lower():
            return json.dumps({"query_variations": [user_prompt + " (paraphrased)"]})
        
        elif "extract" in system_prompt.lower():
            if "battery" in u:
                return json.dumps({
                    "goal": "Follow these steps to perform this Battery Troubleshooting",
                    "title": "Battery optimization",
                    "score": 0.95,
                    "actions": [{
                        "actionName": "Optimize Battery Usage",
                        "description": "It will reduce background power consumption.",
                        "category": "auto",
                        "stepGroups": [{"steps": ["Navigate to Settings.", "Tap Battery.", "Select Optimize."]}]
                    }]
                })
            elif "camera" in u or "blurry" in u:
                return json.dumps({
                    "goal": "Follow these steps to perform this Camera Troubleshooting",
                    "title": "Camera settings reset",
                    "score": 0.90,
                    "actions": [{
                        "actionName": "Reset Camera Settings",
                        "description": "It will restore default camera configurations.",
                        "category": "auto",
                        "stepGroups": [{"steps": ["Open Camera.", "Tap Settings.", "Tap Reset settings."]}]
                    }]
                })
            elif "wifi" in u or "internet" in u:
                return json.dumps({
                    "goal": "Follow these steps to perform this Network Troubleshooting",
                    "title": "Reset network settings",
                    "score": 0.98,
                    "actions": [{
                        "actionName": "Reset Wi-Fi Networks",
                        "description": "It will clear saved network connections.",
                        "category": "critical",
                        "stepGroups": [{"steps": ["Navigate to Settings.", "Tap General management.", "Tap Reset.", "Tap Reset network settings."]}]
                    }]
                })
            else:
                return json.dumps({
                    "goal": "Follow these steps to perform this Swipe Navigation Troubleshooting",
                    "title": "Swipe navigation settings",
                    "score": 0.93,
                    "actions": [{
                        "actionName": "Configure Navigation Bar Settings",
                        "description": "It will let you choose navigation type",
                        "category": "auto",
                        "stepGroups": [{"steps": ["Navigate to Settings.", "Tap Display.", "Tap Navigation bar."]}]
                    }]
                })
            
        elif "deeplink" in system_prompt.lower():
            if "battery" in u: return json.dumps({"selected_deeplink": "bixby://masked/act/device_care"})
            if "camera" in u or "blurry" in u: return json.dumps({"selected_deeplink": "bixby://masked/act/camera_settings"})
            if "wifi" in u or "internet" in u: return json.dumps({"selected_deeplink": "bixby://masked/act/reset_network"})
            return json.dumps({"selected_deeplink": "bixby://masked/act/display_navigation"})
            
        elif "repair" in system_prompt.lower():
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
