import os
import sys
import time
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.cache import check_cache

def test_latency():
    print("Testing Cache Latency (P50, P95)")
    
    # Run at least 30 requests. We will use a semantic variation to ensure it hits Tier 1
    # assuming prewarm has run and cached the original queries and variations.
    
    # Exact match test query
    query_exact = "The mobile phone swipe navigation moves up or down instead of left or right after downloading an app"
    
    # Semantic match test query (one of the paraphrases we mocked in llm.py)
    query_semantic = "Ever since I installed a new app, swiping on my phone scrolls up and down instead of going left or right."
    
    # Warm up (load FAISS and DB)
    check_cache(query_exact)
    
    exact_latencies = []
    semantic_latencies = []
    
    print("Running 30 iterations for exact match...")
    for _ in range(30):
        start = time.perf_counter()
        res = check_cache(query_exact)
        elapsed = (time.perf_counter() - start) * 1000
        exact_latencies.append(elapsed)
        assert res is not None, "Cache miss on exact match!"
        
    print("Running 30 iterations for semantic match...")
    for _ in range(30):
        start = time.perf_counter()
        res = check_cache(query_semantic)
        elapsed = (time.perf_counter() - start) * 1000
        semantic_latencies.append(elapsed)
        assert res is not None, "Cache miss on semantic match!"
        
    print("\n--- RESULTS ---")
    print(f"Exact Match (Tier 0): P50 = {np.percentile(exact_latencies, 50):.2f} ms | P95 = {np.percentile(exact_latencies, 95):.2f} ms")
    print(f"Semantic Match (Tier 1): P50 = {np.percentile(semantic_latencies, 50):.2f} ms | P95 = {np.percentile(semantic_latencies, 95):.2f} ms")
    
    if np.percentile(semantic_latencies, 95) <= 300:
        print("? SUCCESS: Target P95 <= 300 ms met for semantic match.")
    else:
        print("? FAIL: Target P95 <= 300 ms not met.")

if __name__ == "__main__":
    test_latency()
