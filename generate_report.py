import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.pipeline import run_pipeline
from app.cache import init_cache

QUERIES = [
    "My battery dies really fast",
    "Screen glitches and flashes",
    "Swiping navigation is reversed",
    "Camera is blurry",
    "Internet won't connect and wifi drops",
    "The phone is completely frozen",
    "How do I optimize battery usage?",
    "Why is my wifi slow?"
]

def generate_report():
    init_cache()
    report = "# ?? Multi-Scenario Bulk Testing Report\n\n"
    report += "*Below are the results of testing 8 distinct scenarios against the local Guidepost engine.* \n\n"
    
    for q in QUERIES:
        # Pass dummy SIIS text
        res = run_pipeline(q, f"Mocked SIIS response for {q}")
        
        report += f"### ?? Scenario: {q}\n"
        
        ctx = res.get("response", {}).get("contexts", [])
        if not ctx:
            report += f"**Fallback Mode**: {res.get('response', {}).get('fallback', 'no_match')}\n\n"
            continue
            
        c = ctx[0]
        report += f"- **Goal Generated**: {c.get('goal')}\n"
        report += f"- **Title**: {c.get('title')}\n"
        
        actions = c.get("actions", [])
        for act in actions:
            report += f"  - **Action**: {act.get('actionName')} ({act.get('category')})\n"
            dl = act.get("stepGroups", [{}])[0].get("actionableDeepLink")
            if dl:
                report += f"  - **Deeplink Sent to Device**: {dl.get('deeplink')}\n"
                
        report += f"- **Telemetry**: Latency: 0ms (Mock Mode) | Cache Hit: False\n\n"
        report += "---\n\n"
        
    with open("bulk_test_report.md", "w", encoding="utf-8-sig") as f:
        f.write(report)

if __name__ == "__main__":
    generate_report()
