import re
from typing import Dict, Any

URL_PATTERN = re.compile(r'(https?://|www\.)|(\[.*\]\(.*\))', re.IGNORECASE)

def check_no_urls(text: str):
    if URL_PATTERN.search(text):
        raise ValueError(f"URL leak detected in text: {text}")

def validate_goal_syntax(goal: str):
    pattern = r"^Follow these steps to perform this .+ (Troubleshooting|Configuration)$"
    if not re.match(pattern, goal):
        raise ValueError(f"Invalid goal syntax: {goal}")

def validate_title(title: str):
    words = title.strip().split()
    if not (2 <= len(words) <= 3):
        raise ValueError(f"Title must be 2 to 3 words, got {len(words)}: '{title}'")
    if not title[0].isupper():
        raise ValueError(f"Title must be sentence case (starts with uppercase): '{title}'")

def validate_action_name(name: str):
    if name != name.title():
        raise ValueError(f"actionName must be Title Case: '{name}' vs '{name.title()}'")

def validate_action_description(desc: str):
    if not desc.startswith("It will"):
        raise ValueError(f"Description must start with 'It will': '{desc}'")
    words = desc.strip().split()
    # Punctuation might be attached to words, but split() counts tokens.
    if not (5 <= len(words) <= 7):
        raise ValueError(f"Description must be exactly 5 to 7 words, got {len(words)}: '{desc}'")

def validate_score(score: float):
    if not (0.0 <= score <= 1.0):
        raise ValueError(f"Score must be between 0.0 and 1.0, got {score}")

def validate_and_sort_actions(actions: list):
    # Sort auto -> manual -> critical
    order_map = {"auto": 0, "manual": 1, "critical": 2}
    
    for action in actions:
        cat = action.get("category", "manual")
        actionName = action.get("actionName", "")
        desc = action.get("description", "")
        
        check_no_urls(actionName)
        check_no_urls(desc)
        validate_action_name(actionName)
        validate_action_description(desc)
        
        if cat not in order_map:
            raise ValueError(f"Invalid category: {cat}")
            
        step_groups = action.get("stepGroups", [])
        for sg in step_groups:
            for step in sg.get("steps", []):
                check_no_urls(step)
            
            # manual actions MUST NOT carry an actionable deeplink
            if cat == "manual" and sg.get("actionableDeepLink") is not None:
                raise ValueError("manual actions must NOT carry an actionable deeplink")
                
            # If there is a deeplink, check for URL leaks in its description and message
            dl = sg.get("actionableDeepLink")
            if dl:
                check_no_urls(dl.get("description", ""))
                check_no_urls(dl.get("message", ""))
    
    # Check ordering. The PDF asks to sort them. We will sort them in place.
    actions.sort(key=lambda a: order_map.get(a.get("category", "manual"), 99))
    return actions

def validate_response(response_dict: Dict[str, Any]):
    # response_dict should be the "response" object inside the main JSON
    contexts = response_dict.get("contexts", [])
    for ctx in contexts:
        goal = ctx.get("goal", "")
        title = ctx.get("title", "")
        score = ctx.get("score", 0.0)
        
        check_no_urls(goal)
        check_no_urls(title)
        
        validate_goal_syntax(goal)
        validate_title(title)
        validate_score(score)
        
        actions = ctx.get("actions", [])
        validate_and_sort_actions(actions)
        
    return response_dict
