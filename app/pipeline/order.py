import json
from app.llm import call_llm
from app.validate import validate_response

def repair_plan(plan: dict, error_msg: str):
    system = "Fix the JSON to resolve this validation error: " + error_msg
    # In MOCK_LLM mode, llm.py returns the user_prompt directly for "repair"
    res = call_llm(system, json.dumps(plan), json_mode=True)
    try:
        return json.loads(res)
    except:
        return plan

def trim_plan(plan: dict):
    # Programmatic fallback trims to satisfy validation if LLM fails
    for ctx in plan.get("contexts", []):
        # Fix Goal
        goal = ctx.get("goal", "")
        if "Troubleshooting" not in goal and "Configuration" not in goal:
            ctx["goal"] = "Follow these steps to perform this General Troubleshooting"
        
        # Fix Title (2-3 words, sentence case)
        title = ctx.get("title", "Default Title").strip()
        words = title.split()
        if len(words) < 2: words.append("Fix")
        if len(words) > 3: words = words[:3]
        title = " ".join(words)
        ctx["title"] = title[0].upper() + title[1:] if title else "Fix Title"
        
        for act in ctx.get("actions", []):
            # Title Case
            act["actionName"] = act.get("actionName", "Fix Action").title()
            
            # Category
            cat = act.get("category", "manual")
            if cat not in ["auto", "manual", "critical"]:
                act["category"] = "manual"
            if act["category"] == "manual":
                for sg in act.get("stepGroups", []):
                    sg["actionableDeepLink"] = None
                    
            # It will ... (5-7 words)
            desc = act.get("description", "It will solve the issue.")
            if not desc.startswith("It will"):
                desc = "It will " + desc.replace("It will", "").strip()
            d_words = desc.split()
            if len(d_words) < 5:
                d_words.extend(["fix", "the", "problem"][:5 - len(d_words)])
            if len(d_words) > 7:
                d_words = d_words[:7]
            act["description"] = " ".join(d_words)
            
    return plan

def validate_and_repair(plan: dict, max_retries=2):
    current_plan = {"contexts": [plan]}
    for _ in range(max_retries):
        try:
            # We copy because validate_response sorts in-place, don't want side effects if it crashes midway
            import copy
            test_plan = copy.deepcopy(current_plan)
            validated = validate_response(test_plan)
            return validated["contexts"][0]
        except ValueError as e:
            current_plan["contexts"][0] = repair_plan(current_plan["contexts"][0], str(e))
    
    # Trim if still failing
    current_plan = trim_plan(current_plan)
    try:
        current_plan = validate_response(current_plan)
    except ValueError:
        # If it still fails, the trim logic missed something. Return fallback.
        return None
    
    return current_plan["contexts"][0]
