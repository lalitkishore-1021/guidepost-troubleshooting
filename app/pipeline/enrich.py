import json
from app.llm import call_llm

def enrich_query(query: str):
    system = "You are a technical query enricher. Output JSON: {'query_variations': [8 to 10 distinct paraphrased strings]}."
    res = call_llm(system, query, json_mode=True)
    try:
        return json.loads(res).get("query_variations", [])
    except:
        return []
