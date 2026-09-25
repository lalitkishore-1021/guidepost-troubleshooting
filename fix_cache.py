import re

def main():
    with open('app/cache.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the synchronous call with an async to_thread call
    old_call = r"plan = compute_func\(query, \*args\)"
    new_call = r"plan = await asyncio.to_thread(compute_func, query, *args)"
    
    content = re.sub(old_call, new_call, content)

    with open('app/cache.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated get_or_compute to use asyncio.to_thread for non-blocking execution.")

if __name__ == '__main__':
    main()
