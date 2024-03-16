import json

def get_headers(auth_token: str = None, json: bool = False) -> dict:
    """
    Generate headers for HTTP requests.

    Parameters:
        - auth_token (str, optional): Authentication token for authorization.
        - json (bool, optional): If True, sets 'Content-Type' to 'application/json'.

    Returns:
        dict: A dictionary containing the generated headers.

    Example:
        >>> get_headers(auth_token="your_token", json=True)
        {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Bearer your_token'}

        >>> get_headers(auth_token="your_token")
        {'Accept': 'application/json', 'Authorization': 'Bearer your_token'}

        >>> get_headers()
        {'Accept': 'application/json'}
    """
    if auth_token:
        if json:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f"Bearer {auth_token}"
            }
        else:
            headers = {
                'Accept': 'application/json',
                'Authorization': f"Bearer {auth_token}"
            }
    else:
        headers = {
            'Accept': 'application/json'
        }

    return headers

def convert_data(inference_data, convert_to_dict=True):
    """
    Converts the 'data_input', 'data_output', and 'user_comment' fields from JSON strings to dictionaries
    in the provided 'inference_data' object. Automatic conversion is applied if 'convert_to_dict' is True.

    Parameters:
    - inference_data (dict): The input data containing 'data' and potentially 'feedback'.
    - convert_to_dict (bool): A flag indicating whether to automatically convert the fields. Default is True.

    Returns:
    - list: A list of dictionaries containing the converted data.
    """
    if inference_data and inference_data.get('data') and len(inference_data['data']) > 0:
        def is_json_string(data):
            try:
                json.loads(data)
                return True
            except (json.JSONDecodeError, TypeError):
                return False

        converted_data = []

        for d in inference_data.get('data', []):
            if convert_to_dict:
                if is_json_string(d.get('data_input')):
                    d['data_input'] = json.loads(d['data_input'])
                if is_json_string(d.get('data_output')):
                    d['data_output'] = json.loads(d['data_output'])
            if d.get('feedback'):
                for fb in d.get('feedback'):
                    if is_json_string(fb.get('user_comment')):
                        fb['user_comment'] = json.loads(fb['user_comment'])
            
            converted_data.append(d)

        return converted_data
    else:
        return None

def get_response(response, service):
    """
    Processes an HTTP response object and returns the JSON content if the status code is 200.

    Parameters:
        - response (httpx.Response): The response object from an HTTP request.
        - service (str): The name of the service or endpoint called, used in error messages.

    Returns:
        - dict or None: The JSON content of the response if the status code is 200, or None if the status code is 404.

    Raises:
        - Exception: Raised if the status code is 401 or any other code. The error message includes information about the status code, request method, service, and response text.

    Example:
        >>> response = client.get(url, headers=headers)
        >>> result = get_response(response, "ExampleService")
    """
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise Exception("Access Denied: Insufficient Authentication Permissions.")
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"[{response.status_code}] Error {response.request.method} {service} to Trident Trace, {response.text}")
    
def get_url(self, api_endpoint, params=None, api_version=True):
    """
    Generates a complete URL by incorporating the endpoint, API version, and optional parameters.

    Parameters:
        - api_endpoint (str): The endpoint or service path within the API.
        - params (str, optional): Optional parameter to be added to the URL.

    Returns:
        - str: The complete URL consisting of the base URL, API version, endpoint, and optional parameter.

    Example:
        >>> url = get_url("/health")
        >>> print(url)
        "https://baseurl.com/api/v1/health"

        >>> url_params = get_url("/users", params="123")
        >>> print(url_params)
        "https://baseurl.com/api/v1/users/123"
    """
    if api_version:
        base_url = f"{self.base_url}{self.api_version}{api_endpoint}" 
    else:
        base_url = f"{self.base_url}{api_endpoint}"
    
    if params is not None:
        return f"{base_url}/{params}"
    else:
        return base_url

