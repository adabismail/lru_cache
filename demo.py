from lru_cache import LRUCache


RESET  = "\033[0m"
GREEN  = "\033[92m"
RED    = "\033[91m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"


def run(label: str, ops: list[tuple]):
    print(f"\n{BOLD}{CYAN}{'─'*55}{RESET}")
    print(f"{BOLD}{CYAN}  {label}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*55}{RESET}")

    cap   = next(v for op, *v in ops if op == "init")[0]
    cache = LRUCache(cap)
    print(f"  Initialized  LRUCache(capacity={cap})\n")

    for op, *args in ops:
        if op == "init":
            continue

        if op == "put":
            key, val = args
            cache.put(key, val)
            print(f"  {YELLOW}put({key}, {val}){RESET}  →  {cache}")

        elif op == "get":
            key    = args[0]
            result = cache.get(key)
            color  = GREEN if result != -1 else RED
            print(f"  {YELLOW}get({key}){RESET}     →  {color}{result}{RESET}   {cache}")

    print()

if __name__ == "__main__":

    run("LeetCode Example (capacity = 2)", [
        ("init", 2),
        ("put",  1, 1),
        ("put",  2, 2),
        ("get",  1),          # → 1
        ("put",  3, 3),       # evicts key 2
        ("get",  2),          # → -1
        ("put",  4, 4),       # evicts key 1
        ("get",  1),          # → -1
        ("get",  3),          # → 3
        ("get",  4),          # → 4
    ])

    run("Update Refreshes Usage Order (capacity = 2)", [
        ("init", 2),
        ("put",  1, 10),
        ("put",  2, 20),
        ("put",  1, 99),      # update key 1 → it becomes MRU
        ("put",  3, 30),      # key 2 is LRU → evicted
        ("get",  2),          # → -1
        ("get",  1),          # → 99
        ("get",  3),          # → 30
    ])

    run("Capacity = 1 Edge Case", [
        ("init", 1),
        ("put",  1, 100),
        ("get",  1),          # → 100
        ("put",  2, 200),     # evicts 1
        ("get",  1),          # → -1
        ("get",  2),          # → 200
    ])

    run("Eviction Chain (capacity = 3)", [
        ("init", 3),
        ("put",  1, 10),
        ("put",  2, 20),
        ("put",  3, 30),
        ("get",  1),          # 1 → MRU
        ("put",  4, 40),      # evicts 2 (LRU)
        ("get",  2),          # → -1
        ("put",  5, 50),      # evicts 3 (LRU)
        ("get",  3),          # → -1
        ("get",  1),          # → 10
        ("get",  4),          # → 40
        ("get",  5),          # → 50
    ])

    print(f"{BOLD}All demos complete.{RESET}\n")