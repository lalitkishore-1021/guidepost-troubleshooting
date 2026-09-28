import re

def main():
    with open('eval/run_eval.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to inject the JSON generation right before `print("Evaluation complete. results.jsonl and metrics.md generated.")`
    json_export = """
    # --- Generate latest.json ---
    import datetime
    
    # 1. Step Accuracy (No reference dataset comparison implemented in this script)
    step_accuracy = {
        "value": None,
        "unit": "percent",
        "status": "not_measured",
        "correct": 0,
        "total": len(results),
        "formula": "NOT MEASURED - insufficient reference data"
    }
    
    # 2. Deeplink Validity
    deeplink_validity = {
        "value": dl_valid_pct,
        "unit": "percent",
        "status": "PASS" if dl_valid_pct == 100 else "BELOW TARGET",
        "valid": valid_deeplinks,
        "total": total_auto_actions,
        "formula": "valid_deeplinks / total_auto_actions * 100"
    }
    
    # 3. Cache Hit Rate
    actual_cache_hit_rate = (paraphrase_hits / len(HELD_OUT_PARAPHRASES)) * 100 if len(HELD_OUT_PARAPHRASES) > 0 else 0
    cache_hit_rate = {
        "value": actual_cache_hit_rate,
        "unit": "percent",
        "status": "PASS" if actual_cache_hit_rate >= 80 else "BELOW TARGET",
        "hits": paraphrase_hits,
        "misses": len(HELD_OUT_PARAPHRASES) - paraphrase_hits,
        "total": len(HELD_OUT_PARAPHRASES),
        "formula": "paraphrase_hits / total_paraphrase_tests * 100"
    }
    
    # 4. Cached P95 Latency
    all_cache_latencies = exact_cache_latencies + paraphrase_latencies
    overall_p95 = np.percentile(all_cache_latencies, 95) if all_cache_latencies else 0.0
    cached_p95_latency = {
        "value": overall_p95,
        "unit": "ms",
        "status": "PASS" if overall_p95 <= 300 else "BELOW TARGET",
        "samples": len(all_cache_latencies)
    }
    
    # 5. Average Cost Per Query
    average_cost_per_query = {
        "value": avg_cost,
        "unit": "USD",
        "status": "PASS" if avg_cost < 0.05 else "BELOW TARGET",
        "total_cost": total_cost,
        "total_queries": len(results)
    }
    
    # 6. Schema Validity
    schema_validity = {
        "value": schema_valid_pct,
        "unit": "percent",
        "status": "PASS" if schema_valid_pct >= 99 else "BELOW TARGET",
        "valid": schema_valid,
        "invalid": len(results) - schema_valid,
        "total": len(results)
    }
    
    eval_json = {
        "evaluation_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "dataset": "data/queries.json & HELD_OUT_PARAPHRASES",
        "total_cases": len(results) + len(HELD_OUT_PARAPHRASES),
        "step_accuracy": step_accuracy,
        "deeplink_validity": deeplink_validity,
        "cache_hit_rate": cache_hit_rate,
        "cached_p95_latency": cached_p95_latency,
        "average_cost_per_query": average_cost_per_query,
        "schema_validity": schema_validity
    }
    
    os.makedirs(EVAL_DIR / "results", exist_ok=True)
    with open(EVAL_DIR / "results" / "latest.json", "w", encoding="utf-8") as f:
        json.dump(eval_json, f, indent=2)
"""
    
    # Insert JSON export block
    content = content.replace('print("Evaluation complete.', json_export + '\n    print("Evaluation complete.')
    
    with open('eval/run_eval.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
