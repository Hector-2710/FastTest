import json

@staticmethod
def print_report(result, url, status, body, error_msg=None):
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
        
        print(f"{bold}Body:{reset}")
        # Pretty Print JSON
        try:
            if isinstance(body, (dict, list)):
                content = json.dumps(body, indent=4, ensure_ascii=False)
                print(content)
            else:
                # Si es texto, tratamos de ver si es un string que parece JSON
                try:
                    loaded = json.loads(body)
                    print(json.dumps(loaded, indent=4, ensure_ascii=False))
                except:
                    print(body)
        except:
            print(body)
            
        print(f"{color}{'='*60}{reset}\n")
