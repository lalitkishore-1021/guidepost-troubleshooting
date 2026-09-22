import json
import urllib.request
import urllib.error

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

URL = "http://127.0.0.1:8000/v1/troubleshoot"

print("# ?? Bulk Scenario Testing Report\n")
print("*Below are the results of testing various scenarios against the local Guidepost API.*\n")

for q in QUERIES:
    req = urllib.request.Request(
        URL, 
        data=json.dumps({"query": q, "siis_response": "Mocked kb text..."}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            print(f"### Scenario: {q}")
            
            ctx = res_data.get("response", {}).get("contexts", [])
            if not ctx:
                print(f"**Fallback Mode**: {res_data.get('response', {}).get('fallback', 'no_match')}\n")
                continue
                
            c = ctx[0]
            print(f"- **Goal Generated**: {c.get('goal')}")
            print(f"- **Title**: {c.get('title')}")
            
            actions = c.get("actions", [])
            for act in actions:
                print(f"  - **Action**: {act.get('actionName')} ({act.get('category')})")
                dl = act.get("stepGroups", [{}])[0].get("actionableDeepLink")
                if dl:
                    print(f"  - **Deeplink Sent to Device**: {dl.get('deeplink')}")
                    
            print(f"- **Telemetry**: Latency: {res_data.get('meta', {}).get('latency_ms')}ms | Cache Hit: {res_data.get('meta', {}).get('cache_hit')}")
            print("\n---\n")
            
    except Exception as e:
        print(f"### Scenario: {q}\n**Error:** {e}\n\n---\n")
