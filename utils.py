import json

def print_report(result: str, url: str, status: int, body: any, error_msg: str = None):
    color = "\033[92m" if result == "PASSED" else "\033[91m"
    reset = "\033[0m"
    bold = "\033[1m"
    
    print(f"\n{color}{bold}{'='*60}{reset}")
    print(f"{color}{bold} TEST {result} {reset}")
    print(f"{color}{'='*60}{reset}")
    print(f"{bold}URL:{reset}    {url}")
    print(f"{bold}Status:{reset} {status}")
    
    if error_msg:
        print(f"{bold}Error:{reset}  {error_msg}")
    
    if body:
        print(f"{bold}Body:{reset}")
        print(json.dumps(body, indent=4, ensure_ascii=False))
    
    print(f"{color}{'='*60}{reset}\n")

