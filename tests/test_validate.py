import json
import pytest
from pathlib import Path
import sys
import os

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.validate import (
    validate_response,
    validate_goal_syntax,
    validate_title,
    validate_action_name,
    validate_action_description,
    check_no_urls,
    validate_and_sort_actions
)

SAMPLES_DIR = Path(__file__).parent.parent / "data" / "samples"

def test_samples_pass():
    for i in range(1, 6):
        sample_path = SAMPLES_DIR / f"sample{i}.json"
        with open(sample_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        
        # Should not raise any exception
        validate_response(data["response"])

def test_url_leak():
    with pytest.raises(ValueError, match="URL leak detected"):
        check_no_urls("Here is a link http://samsung.com")
    with pytest.raises(ValueError, match="URL leak detected"):
        check_no_urls("Visit www.samsung.com")
    with pytest.raises(ValueError, match="URL leak detected"):
        check_no_urls("Check [this](https://link.com)")

def test_goal_syntax():
    # Pass
    validate_goal_syntax("Follow these steps to perform this Display Troubleshooting")
    validate_goal_syntax("Follow these steps to perform this Network Configuration")
    
    # Fail
    with pytest.raises(ValueError):
        validate_goal_syntax("These are the steps for Display Troubleshooting")

def test_title():
    # Pass
    validate_title("Swipe navigation settings") # 3 words, sentence case
    validate_title("Network config") # 2 words, sentence case
    
    # Fail word count
    with pytest.raises(ValueError, match="Title must be 2 to 3 words"):
        validate_title("Settings")
    with pytest.raises(ValueError, match="Title must be 2 to 3 words"):
        validate_title("This is a very long title")
        
    # Fail sentence case (lowercase first letter)
    with pytest.raises(ValueError, match="Title must be sentence case"):
        validate_title("swipe navigation settings")

def test_action_name():
    # Pass
    validate_action_name("Configure Navigation Bar Settings")
    
    # Fail
    with pytest.raises(ValueError, match="actionName must be Title Case"):
        validate_action_name("Configure navigation bar settings")

def test_action_description():
    # Pass (5 words)
    validate_action_description("It will fix the screen.")
    # Pass (7 words)
    validate_action_description("It will let you choose navigation type.")
    
    # Fail prefix
    with pytest.raises(ValueError, match="Description must start with 'It will'"):
        validate_action_description("This will fix the screen.")
        
    # Fail word count (<5)
    with pytest.raises(ValueError, match="exactly 5 to 7 words"):
        validate_action_description("It will fix it.")
        
    # Fail word count (>7)
    with pytest.raises(ValueError, match="exactly 5 to 7 words"):
        validate_action_description("It will let you choose navigation type safely now.")

def test_category_ordering_and_manual_rule():
    actions = [
        {
            "actionName": "Critical Action",
            "description": "It will reset the entire device.",
            "category": "critical",
            "stepGroups": []
        },
        {
            "actionName": "Manual Action",
            "description": "It will clean the charging port.",
            "category": "manual",
            "stepGroups": [{"actionableDeepLink": {"deeplink": "bixby://masked/act/fake"}}]
        },
        {
            "actionName": "Auto Action",
            "description": "It will open the display settings.",
            "category": "auto",
            "stepGroups": []
        }
    ]
    
    # manual action with actionableDeepLink should fail
    with pytest.raises(ValueError, match="manual actions must NOT carry an actionable deeplink"):
        validate_and_sort_actions(actions)
        
    # fix the manual action
    actions[1]["stepGroups"][0]["actionableDeepLink"] = None
    
    # Now it should sort them: auto -> manual -> critical
    sorted_actions = validate_and_sort_actions(actions)
    assert sorted_actions[0]["category"] == "auto"
    assert sorted_actions[1]["category"] == "manual"
    assert sorted_actions[2]["category"] == "critical"
