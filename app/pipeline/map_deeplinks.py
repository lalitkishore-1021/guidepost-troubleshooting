import json
from app.llm import call_llm
from app.retrieval import get_retriever

def map_deeplinks(plan: dict):
    if not plan:
        return plan
        
    retriever = get_retriever()
    catalog = {item['deeplink']: item for item in retriever.catalog}
    
    for action in plan.get("actions", []):
        cat = action.get("category", "manual")
        if cat == "manual":
            for sg in action.get("stepGroups", []):
                sg["actionableDeepLink"] = None
            continue
        
        query = f"{action.get('actionName','')} {action.get('description','')}"
        candidates = retriever.search(query, top_k=5)
        if not candidates:
            continue
        
        system = "Select the best matching deeplink ID from the candidates. Output JSON: {'selected_deeplink': 'id'}. Use 'bixby://dummy_positive' only if none match."
        user = f"Query: {query}\nCandidates:\n"
        for c in candidates:
            user += f"- ID: {c['deeplink']}, Desc: {c['entry'].get('description','')}\n"
        
        res = call_llm(system, user, json_mode=True)
        try:
            selected = json.loads(res).get("selected_deeplink")
            if selected in catalog:
                entry = catalog[selected]
                for sg in action.get("stepGroups", []):
                    sg["actionableDeepLink"] = {
                        "deeplink": selected,
                        "description": entry.get("description", ""),
                        "message": entry.get("message", "")
                    }
            elif selected == "bixby://dummy_positive":
                for sg in action.get("stepGroups", []):
                    sg["actionableDeepLink"] = {
                        "deeplink": selected,
                        "description": "Placeholder",
                        "message": "Placeholder"
                    }
        except:
            pass
    return plan
