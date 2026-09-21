import json
from pathlib import Path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.retrieval import get_retriever

SAMPLES_DIR = Path(__file__).parent.parent / "data" / "samples"

def main():
    print("Loading retriever (this may take a moment to download the model)...")
    retriever = get_retriever()
    print("Retriever loaded successfully.")
    
    total_queries = 0
    top1_hits = 0
    top3_hits = 0
    misses = []
    
    for i in range(1, 6):
        sample_path = SAMPLES_DIR / f"sample{i}.json"
        if not sample_path.exists(): continue
        with open(sample_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            
        for ctx in data.get("response", {}).get("contexts", []):
            for action in ctx.get("actions", []):
                action_text = f"{action.get('actionName', '')} {action.get('description', '')}"
                
                for sg in action.get("stepGroups", []):
                    dl = sg.get("actionableDeepLink")
                    if dl and dl.get("deeplink"):
                        target_uri = dl.get("deeplink")
                        
                        # Perform search
                        results = retriever.search(action_text, top_k=3)
                        retrieved_uris = [res["deeplink"] for res in results]
                        
                        total_queries += 1
                        if target_uri in retrieved_uris:
                            top3_hits += 1
                            if target_uri == retrieved_uris[0]:
                                top1_hits += 1
                            else:
                                misses.append((action_text, target_uri, retrieved_uris, "Missed Top-1 (Found in Top-3)"))
                        else:
                            misses.append((action_text, target_uri, retrieved_uris, "Missed Top-3"))
                            
    print(f"\nTotal: {total_queries}")
    if total_queries > 0:
        print(f"Top-1 Accuracy: {top1_hits/total_queries*100:.2f}%")
        print(f"Top-3 Accuracy: {top3_hits/total_queries*100:.2f}%")
    
    if misses:
        print("\nMisses:")
        for m in misses:
            print(f"Query: {m[0]}\nTarget: {m[1]}\nRetrieved: {m[2]}\nStatus: {m[3]}\n")
    else:
        print("\nNo misses! Perfect accuracy on samples.")

if __name__ == "__main__":
    main()
