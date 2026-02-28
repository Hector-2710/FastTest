import requests
from typing import Optional, Dict, Any, Annotated, Union
from rapidtest.Utils import print_report, show_connection_error


class Test:
    """
    Clase principal para realizar pruebas de integración en APIs REST.
    
    Esta clase permite realizar peticiones HTTP y validar automáticamente 
    el código de estado y el cuerpo de la respuesta.
    """

    def __init__(self, *,
        url: Annotated[str, "La URL base de la API (ej: 'http://localhost:8000')"]):
        """
        Inicializa el cliente de pruebas.

        Args:
            url (str): La URL base de la API (ej: 'http://localhost:8000').
        """
        self.url = url.rstrip('/')

    def _request(
        self, 
        method: Annotated[str, "Método HTTP (GET, POST, etc.)"], 
        endpoint: Annotated[str, "Ruta del endpoint (ej: '/users')"], 
        expected_status: Annotated[int, "Código de estado HTTP esperado"] = 200, 
        expected_body: Optional[Dict[str, Any]] = None,
        json: Optional[Union[Dict[str, Any], list, str, int, float, bool]] = None,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Optional[requests.Response]:
        """
        Método interno para realizar peticiones y validar resultados.

        Args:
            method (str): Método HTTP (GET, POST, etc.).
            endpoint (str): Ruta del endpoint (ej: '/users').
            expected_status (int): Código de estado HTTP esperado.
            expected_body (dict, optional): Cuerpo JSON esperado en la respuesta.
            json (dict/list/str/int/float/bool, optional): Datos JSON a enviar en el cuerpo de la petición.
            data (str/bytes/dict, optional): Datos del cuerpo de la petición.
            params (dict, optional): Parámetros de consulta para la URL.
            headers (dict, optional): Cabeceras HTTP adicionales.
            **kwargs: Argumentos adicionales para requests (timeout, cookies, etc.).

        Returns:
            requests.Response: El objeto de respuesta si la conexión fue exitosa.
            None: Si ocurrió un error crítico de conexión.
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
        """Realiza una petición GET y valida el resultado."""
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
        """Realiza una petición POST y valida el resultado."""
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
        """Realiza una petición PUT y valida el resultado."""
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
        """Realiza una petición PATCH y valida el resultado."""
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
        """Realiza una petición DELETE y valida el resultado."""
        return self._request("DELETE", endpoint, expected_status, expected_body, 
                           json=json, data=data, params=params, headers=headers, **kwargs)


    