import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.cache import save_to_cache, check_cache
from app.pipeline import run_pipeline

DATA_DIR = Path(__file__).parent.parent / "data"

def prewarm():
    print("Pre-warming cache from data/queries.json...")
    with open(DATA_DIR / "queries.json", "r", encoding="utf-8-sig") as f:
        queries = json.load(f)
        
    # We will use mock SIIS responses to prewarm
    with open(DATA_DIR / "siis_responses.json", "r", encoding="utf-8-sig") as f:
        siis_data = json.load(f)
    siis_dict = {f"siis_{i+1}": item["text"] for i, item in enumerate(siis_data)}
    
    for idx, q_obj in enumerate(queries):
        query = q_obj["query"]
        if check_cache(query):
            print(f"[{idx+1}/{len(queries)}] Already in cache: {query}")
            continue
            
        print(f"[{idx+1}/{len(queries)}] Running pipeline for: {query}")
        
        # Pick a mock SIIS matching domain loosely or just the first one
        siis_text = list(siis_dict.values())[idx % len(siis_dict)]
        
        plan = run_pipeline(query, siis_text)
        if plan and len(plan["response"].get("contexts", [])) > 0:
            save_to_cache(query, plan.get("query_variations", []), plan)
            
    print("Pre-warming complete!")

if __name__ == "__main__":
    prewarm()
