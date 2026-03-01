import requests
from typing import Optional, Dict, Any, Annotated, Union
from rapidtest.Utils import print_report, show_connection_error

class Test:
    """
    Main class for performing REST API integration tests.
    
    This class allows making HTTP requests and automatically validating 
    status codes and response bodies.
    """

    def __init__(self, *,
        url: Annotated[str, "The base URL of the API (e.g., 'http://localhost:8000')"]):
        """
        Initializes the test client.

        Args:
            url (str): The base URL of the API (e.g., 'http://localhost:8000').
        """
        self.url = url.rstrip('/')

    def _request(
        self, 
        method: Annotated[str, "HTTP method (GET, POST, etc.)"], 
        endpoint: Annotated[str, "Endpoint path (e.g., '/users')"], 
        expected_status: Annotated[int, "Expected HTTP status code"] = 200, 
        expected_body: Optional[Dict[str, Any]] = None,
        json: Optional[Union[Dict[str, Any], list, str, int, float, bool]] = None,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Optional[requests.Response]:
        """
        Internal method to make requests and validate results.

        Args:
            method (str): HTTP method (GET, POST, etc.).
            endpoint (str): Endpoint path (e.g., '/users').
            expected_status (int): Expected HTTP status code.
            expected_body (dict, optional): Expected JSON body in response.
            json (dict/list/str/int/float/bool, optional): JSON data to send in request body.
            data (str/bytes/dict, optional): Request body data.
            params (dict, optional): Query parameters for the URL.
            headers (dict, optional): Additional HTTP headers.
            **kwargs: Additional arguments for requests (timeout, cookies, etc.).

        Returns:
            requests.Response: The response object if connection was successful.
            None: If a critical connection error occurred.
        """
        url = f"{self.url}/{endpoint.lstrip('/')}"
        method_func = getattr(requests, method.lower())
        
        request_kwargs = {}
        if json is not None:
            request_kwargs['json'] = json
        if data is not None:
            request_kwargs['data'] = data
        if params is not None:
            request_kwargs['params'] = params
        if headers is not None:
            request_kwargs['headers'] = headers
        
        request_kwargs.update(kwargs)
        
        try:
            response = method_func(url, **request_kwargs)
            status_ok = response.status_code == expected_status
            body_ok = True
            error_msg = None
            
            response_json = None
            try:
                response_json = response.json()
            except Exception:
                response_json = {"raw_content": response.text}
            
        
            if expected_body is not None:
                if response_json != expected_body:
                    body_ok = False
                    if status_ok:
                        error_msg = "The expected body is not the correct"
                    else:
                        error_msg = f"Expected status {expected_status}, but got {response.status_code} and the expected body is not the correct"

            if not status_ok and not error_msg:
                error_msg = f"Expected status {expected_status}, but got {response.status_code}"

            if status_ok and body_ok:
                print_report("PASSED", response.url, response.status_code, response_json)
            else:
                print_report("FAILED", response.url, response.status_code, response_json, error_msg=error_msg)

            return response
            
        except Exception as e:
            show_connection_error(url, e)
            return None

    def get(self, *, 
            endpoint: str, 
            expected_status: int = 200, 
            expected_body: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs) -> Optional[requests.Response]:
        """Performs a GET request and validates the result."""
        return self._request("GET", endpoint, expected_status, expected_body, 
                           params=params, headers=headers, **kwargs)

    def post(self, *, 
             endpoint: str, 
             expected_status: int = 201, 
             expected_body: Optional[Dict[str, Any]] = None,
             json: Optional[Union[Dict[str, Any], list, str, int, float, bool]] = None,
             data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
             params: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None,
             **kwargs) -> Optional[requests.Response]:
        """Performs a POST request and validates the result."""
        return self._request("POST", endpoint, expected_status, expected_body, 
                           json=json, data=data, params=params, headers=headers, **kwargs)

    def put(self, *, 
            endpoint: str, 
            expected_status: int = 200, 
            expected_body: Optional[Dict[str, Any]] = None,
            json: Optional[Union[Dict[str, Any], list, str, int, float, bool]] = None,
            data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            **kwargs) -> Optional[requests.Response]:
        """Performs a PUT request and validates the result."""
        return self._request("PUT", endpoint, expected_status, expected_body, 
                           json=json, data=data, params=params, headers=headers, **kwargs)

    def patch(self, *, 
              endpoint: str, 
              expected_status: int = 200, 
              expected_body: Optional[Dict[str, Any]] = None,
              json: Optional[Union[Dict[str, Any], list, str, int, float, bool]] = None,
              data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
              params: Optional[Dict[str, Any]] = None,
              headers: Optional[Dict[str, str]] = None,
              **kwargs) -> Optional[requests.Response]:
        """Performs a PATCH request and validates the result."""
        return self._request("PATCH", endpoint, expected_status, expected_body, 
                           json=json, data=data, params=params, headers=headers, **kwargs)

    def delete(self, *, 
               endpoint: str, 
               expected_status: int = 204, 
               expected_body: Optional[Dict[str, Any]] = None,
               json: Optional[Union[Dict[str, Any], list, str, int, float, bool]] = None,
               data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
               params: Optional[Dict[str, Any]] = None,
               headers: Optional[Dict[str, str]] = None,
               **kwargs) -> Optional[requests.Response]:
        """Performs a DELETE request and validates the result."""
        return self._request("DELETE", endpoint, expected_status, expected_body, 
                           json=json, data=data, params=params, headers=headers, **kwargs)


    