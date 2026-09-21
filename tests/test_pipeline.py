import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.pipeline import run_pipeline

def test_mock_pipeline():
    query = "The mobile phone swipe navigation moves up or down instead of left or right after downloading an app"
    siis_text = "If you are experiencing issues with swipe navigation gestures scrolling incorrectly, you can configure the Navigation Bar Settings..."
    
    result = run_pipeline(query, siis_text)
    
    assert result["query"] == query
    assert len(result["query_variations"]) > 0
    assert len(result["response"]["contexts"]) == 1
    
    ctx = result["response"]["contexts"][0]
    assert ctx["goal"] == "Follow these steps to perform this Swipe Navigation Troubleshooting"
    assert len(ctx["actions"]) > 0
    
    action = ctx["actions"][0]
    assert action["category"] == "auto"
    assert action["actionName"] == "Configure Navigation Bar Settings"
    assert action["description"] == "It will let you choose navigation type"
    
    dl = action["stepGroups"][0]["actionableDeepLink"]
    assert dl["deeplink"] == "bixby://masked/act/display_navigation"
    
    # Cost should be > 0 or 0 depending on env, but we just verify it exists
    assert "latency_ms" in result["meta"]
    assert "cost_usd" in result["meta"]

if __name__ == "__main__":
    test_mock_pipeline()
    print("Mock pipeline works successfully!")
