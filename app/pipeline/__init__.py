from .enrich import enrich_query
from .extract import extract_plan
from .map_deeplinks import map_deeplinks
from .order import validate_and_repair
from app.llm import reset_stats, usage_stats

def run_pipeline(query: str, siis_response: str = None):
    reset_stats()
    
    # If no siis_response, Honest Failure
    if not siis_response:
        return {
            "query": query,
            "query_variations": [],
            "response": {"contexts": [], "fallback": "no_match"},
            "meta": usage_stats.copy()
        }

    variations = enrich_query(query)
    plan = extract_plan(siis_response)
    
    if not plan:
        return {
            "query": query, 
            "query_variations": variations, 
            "response": {"contexts": [], "fallback": "no_match"}, 
            "meta": usage_stats.copy()
        }
        
    plan = map_deeplinks(plan)
    final_plan = validate_and_repair(plan)
    
    if not final_plan:
        return {
            "query": query, 
            "query_variations": variations, 
            "response": {"contexts": [], "fallback": "no_match"}, 
            "meta": usage_stats.copy()
        }
    
    return {
        "query": query,
        "query_variations": variations,
        "response": {"contexts": [final_plan]},
        "meta": usage_stats.copy()
    }
