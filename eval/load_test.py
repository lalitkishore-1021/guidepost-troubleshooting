import asyncio
import time
import sys

try:
    import httpx
except ImportError:
    print("Please install httpx: pip install httpx")
    sys.exit(1)

URL = "http://127.0.0.1:8000/v1/troubleshoot"
RPS = 50
DURATION = 10
QUERIES = [
    "My battery dies really fast",
    "Screen glitches and flashes",
    "Swiping navigation is reversed"
]

async def fetch(client, query):
    try:
        res = await client.post(URL, json={"query": query}, timeout=10.0)
        return res.status_code
    except Exception:
        return 0

async def worker(client, query, delay):
    await asyncio.sleep(delay)
    return await fetch(client, query)

async def main():
    print(f"Starting Load Test: {RPS} RPS for {DURATION} seconds...")
    tasks = []
    
    # Increase limits for load testing
    limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)
    
    async with httpx.AsyncClient(limits=limits) as client:
        # Pre-warm connection
        await client.get("http://127.0.0.1:8000/health")
        
        start_time = time.time()
        for second in range(DURATION):
            for i in range(RPS):
                query = QUERIES[i % len(QUERIES)]
                # distribute requests evenly across the second
                delay = second + (i / RPS)
                tasks.append(asyncio.create_task(worker(client, query, delay)))
        
        print(f"Dispatched {len(tasks)} requests. Waiting for completion...")
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start_time
        
    success = sum(1 for r in results if r == 200)
    failed = len(results) - success
    
    print("\n--- Load Test Results ---")
    print(f"Total Requests: {len(results)}")
    print(f"Success (200 OK): {success}")
    print(f"Failed / Timeout: {failed}")
    print(f"Success Rate: {(success/len(results))*100:.2f}%")
    print(f"Effective RPS: {len(results)/elapsed:.2f}")

if __name__ == "__main__":
    # Windows fix for Event Loop policy with many connections
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
