import sqlite3
import json
import os
import numpy as np
import asyncio
import faiss
from sentence_transformers import SentenceTransformer

DB_PATH = "cache.db"
SIMILARITY_THRESHOLD = 0.90

_model = None
_db_conn = None
_faiss_index = None
_cache_mapping = []

_in_flight = {}
_in_flight_lock = asyncio.Lock()

def get_db():
    global _db_conn
    if _db_conn is None:
        _db_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _db_conn.execute('''CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exact_query TEXT UNIQUE,
            plan_json TEXT
        )''')
        _db_conn.execute('''CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id INTEGER,
            variation TEXT,
            embedding BLOB,
            FOREIGN KEY(plan_id) REFERENCES plans(id)
        )''')
        _db_conn.commit()
    return _db_conn

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    return _model

def load_faiss():
    global _faiss_index, _cache_mapping
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT plan_id, embedding FROM embeddings")
    rows = cursor.fetchall()
    
    dim = 384
    _faiss_index = faiss.IndexFlatIP(dim)
    _cache_mapping = []
    
    if rows:
        vecs = []
        for plan_id, emb_blob in rows:
            vec = np.frombuffer(emb_blob, dtype=np.float32)
            vecs.append(vec)
            _cache_mapping.append(plan_id)
        
        vecs_np = np.vstack(vecs)
        faiss.normalize_L2(vecs_np)
        _faiss_index.add(vecs_np)

def init_cache():
    get_db()
    get_model()
    load_faiss()

def check_cache(query: str):
    if _faiss_index is None:
        init_cache()
        
    db = get_db()
    cursor = db.cursor()
    
    # Tier 0: Exact match
    cursor.execute("SELECT plan_json FROM plans WHERE exact_query = ?", (query.lower(),))
    row = cursor.fetchone()
    if row:
        return json.loads(row[0])
        
    # Tier 1: Semantic match
    if _faiss_index.ntotal > 0:
        query_emb = get_model().encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_emb)
        D, I = _faiss_index.search(query_emb, 1)
        
        if len(D) > 0 and len(D[0]) > 0 and D[0][0] >= SIMILARITY_THRESHOLD:
            best_idx = I[0][0]
            plan_id = _cache_mapping[best_idx]
            cursor.execute("SELECT plan_json FROM plans WHERE id = ?", (plan_id,))
            plan_row = cursor.fetchone()
            if plan_row:
                return json.loads(plan_row[0])
    
    return None

def save_to_cache(exact_query: str, variations: list, plan_dict: dict):
    if _faiss_index is None:
        init_cache()
        
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO plans (exact_query, plan_json) VALUES (?, ?)", 
                       (exact_query.lower(), json.dumps(plan_dict)))
        plan_id = cursor.lastrowid
        
        all_texts = [exact_query] + variations
        embs = get_model().encode(all_texts, convert_to_numpy=True)
        
        for i, text in enumerate(all_texts):
            cursor.execute("INSERT INTO embeddings (plan_id, variation, embedding) VALUES (?, ?, ?)",
                           (plan_id, text, embs[i].tobytes()))
        db.commit()
        
        # Update FAISS in memory
        faiss.normalize_L2(embs)
        _faiss_index.add(embs)
        _cache_mapping.extend([plan_id] * len(all_texts))
        
    except sqlite3.IntegrityError:
        pass # Already exists

async def get_or_compute(query: str, compute_func, *args):
    import time
    start = time.time()
    
    # Check cache first
    hit = check_cache(query)
    if hit:
        hit["meta"]["cache_hit"] = True
        hit["meta"]["latency_ms"] = int((time.time() - start) * 1000)
        hit["meta"]["cost_usd"] = 0.0
        return hit
        
    # Request Coalescing
    async with _in_flight_lock:
        if query in _in_flight:
            event = _in_flight[query]
            is_leader = False
        else:
            event = asyncio.Event()
            _in_flight[query] = event
            is_leader = True
            
    if not is_leader:
        await event.wait()
        hit = check_cache(query)
        if hit:
            hit["meta"]["cache_hit"] = True
            hit["meta"]["latency_ms"] = int((time.time() - start) * 1000)
            hit["meta"]["cost_usd"] = 0.0
            return hit
        return None
        
    # Leader computes
    try:
        plan = compute_func(query, *args)
        if plan and "response" in plan and len(plan["response"].get("contexts", [])) > 0:
            save_to_cache(query, plan.get("query_variations", []), plan)
            plan["meta"]["cache_hit"] = False
        return plan
    finally:
        event.set()
        async with _in_flight_lock:
            del _in_flight[query]
