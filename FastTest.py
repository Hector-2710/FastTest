from requests import get
from utils import print_report

class FastTest:
    def __init__(self, url: str):
        self.url = url

    def get(self, endpoint: str, expected_status: int = 200, expected_body: dict = None, params: dict = None, headers: dict = None, **kwargs):
        url = f"{self.url}{endpoint}"
        
        try:
            response = get(url, params=params, headers=headers, **kwargs)
            actual_url = response.url
            actual_status = response.status_code
            actual_body = response.json()

            status_ok = actual_status == expected_status
            body_ok = True
            error_msg = None

            if expected_body is not None:
                if actual_body != expected_body:
                    body_ok = False
                    error_msg = f"Expected status {expected_status}, but got {actual_status}. " if not status_ok else ""
                    error_msg += f"Body mismatch."

            if not status_ok and not error_msg:
                error_msg = f"Expected status {expected_status}, but got {actual_status}"

            if status_ok and body_ok:
                print_report("PASSED", actual_url, actual_status, actual_body)
            else:
                print_report("FAILED", actual_url, actual_status, actual_body, error_msg=error_msg)

            return response
            

        except Exception as e:
            print(f"\n❌ CRITICAL ERROR connecting to {url}: {str(e)}")
            return None

   

    