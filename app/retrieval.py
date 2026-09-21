import json
import os
import numpy as np
from pathlib import Path
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util

DATA_DIR = Path(__file__).parent.parent / "data"
DEEPLINKS_FILE = DATA_DIR / "deeplinks.json"

class HybridRetriever:
    def __init__(self, deeplinks_path=DEEPLINKS_FILE):
        with open(deeplinks_path, "r", encoding="utf-8-sig") as f:
            self.catalog = json.load(f)
        
        self.corpus = []
        for item in self.catalog:
            # Combine fields, ignore URI string
            desc = item.get("description", "")
            msg = item.get("message", "")
            qna = item.get("qna_description", "")
            text = f"{desc} {msg} {qna}".strip()
            self.corpus.append(text)
        
        # BM25 setup
        tokenized_corpus = [doc.lower().split() for doc in self.corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)
        
        # Embeddings setup
        self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        self.embeddings = self.model.encode(self.corpus, convert_to_tensor=True)
        
    def search(self, query: str, top_k: int = 5):
        # Prevent top_k > catalog size
        top_k = min(top_k, len(self.corpus))
        
        # BM25 scores
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_ranks = np.argsort(bm25_scores)[::-1]
        
        # Semantic scores
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0].cpu().numpy()
        semantic_ranks = np.argsort(cos_scores)[::-1]
        
        # RRF (Reciprocal Rank Fusion)
        rrf_scores = np.zeros(len(self.corpus))
        k = 60 # RRF constant
        
        for rank, doc_idx in enumerate(bm25_ranks):
            rrf_scores[doc_idx] += 1.0 / (k + rank + 1)
            
        for rank, doc_idx in enumerate(semantic_ranks):
            rrf_scores[doc_idx] += 1.0 / (k + rank + 1)
            
        final_ranks = np.argsort(rrf_scores)[::-1]
        
        results = []
        for idx in final_ranks[:top_k]:
            results.append({
                "deeplink": self.catalog[idx]["deeplink"],
                "score": float(rrf_scores[idx]),
                "entry": self.catalog[idx]
            })
            
        return results

# Singleton instance initialized at startup
retriever = None

def get_retriever():
    global retriever
    if retriever is None:
        retriever = HybridRetriever()
    return retriever
