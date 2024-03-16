import httpx
import json
from slugify import slugify
from .utils import get_headers, get_response, get_url

class CoreAPI:
    def __init__(self, base_url, auth_token, api_version="/api/v1") -> None:
        self.base_url = base_url
        self.auth_token = auth_token
        self.api_version = api_version

    def get_health(self) -> dict:
        api_endpoint = "/health" 
        url = get_url(self, api_endpoint, api_version=False)
        headers = get_headers()
        with httpx.Client() as client:
            response = client.get(url, headers=headers)
        return get_response(response, "Health")['success'] 
        
    # Domain Service
    def get_domain(self, app_name) -> dict:
        api_endpoint = "/domain"
        url = get_url(self, api_endpoint, params=slugify(app_name))
        headers = get_headers(self.auth_token)
        with httpx.Client() as client:
            response = client.get(url=url, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data')
            return data['id'], data['slug'] if data else (None, None)
        else:
            return None, None

    def post_domain(self, app_name) -> str | dict:
        api_endpoint = "/domain"
        url = get_url(self, api_endpoint) 
        headers = get_headers(self.auth_token, json=True)
        payload = {'name': f"{app_name}"}
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=payload)
        return get_response(response, "Domain").get('data', {})

    def delete_domain(self, domain_id):
        api_endpoint = "/domain"
        url = get_url(self, api_endpoint, params=domain_id)
        headers = get_headers(self.auth_token)
        with httpx.Client() as client:
            response = client.delete(url, headers=headers)
        return get_response(response, "Domain")['success']

    # Inference Service
    def get_list_inference(self, **kwargs):
        api_endpoint = f"{self.api_version}/inference"
        url = f"{self.base_url}{api_endpoint}"
        headers = get_headers(self.auth_token)
        filtered_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        if filtered_kwargs:
            url += "?" + "&".join(f"{key}={value}" for key, value in filtered_kwargs.items())
        with httpx.Client() as client:
            response = client.get(url, headers=headers)
        return get_response(response, "List Inference")

    def get_detail_inference(self, inference_uuid):
        api_endpoint = "/inference"
        url = get_url(self, api_endpoint, inference_uuid)
        headers = get_headers(self.auth_token)
        with httpx.Client() as client:
            response = client.get(url, headers=headers)
        return get_response(response, "Detail Inference")
        
    def post_inference(self, body):
        api_endpoint = "/inference"
        url = get_url(self, api_endpoint)
        headers = get_headers(self.auth_token, json=True)
        payload = body
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=payload)  
        return get_response(response, "Inference")
        
    def delete_inference(self, inference_uuid):
        api_endpoint = "/inference"
        url = get_url(self, api_endpoint, params=inference_uuid)
        headers = get_headers(self.auth_token)
        with httpx.Client() as client:
            response = client.delete(url, headers=headers)
        return get_response(response, "Inference")['success']
        
    def get_group_inference(self, **kwargs):
        api_endpoint = "/inference/group"
        url = get_url(self, api_endpoint)
        headers = get_headers(self.auth_token)
        params = {key:value for key, value in dict(**kwargs).items() if value is not None}
        with httpx.Client() as client:
            response = client.get(url, headers=headers, params=params)
        return get_response(response, "List Group Inference")
        
    def get_detail_group_inference(self, group_id):
        api_endpoint = "/inference/group"
        url = get_url(self, api_endpoint, group_id)
        headers = get_headers(self.auth_token)
        with httpx.Client() as client:
            response = client.get(url, headers=headers)
        return get_response(response, "Detail Group Inference")
        
    # Feedback Service
    def post_feedback(self, inference_uuid, user_reaction, user_comment, user):
        api_endpoint = "/feedback"
        url = get_url(self, api_endpoint)
        headers = get_headers(self.auth_token, json=True)
        payload = {
            "inference_uuid": inference_uuid,
            "user": user,
            "user_reaction": 1 if user_reaction else 0,
            "user_comment": json.dumps(user_comment) if isinstance(user_comment, dict) else user_comment, 
        }
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=payload)
        return get_response(response, "Feedback")
    
    def update_feedback(self, uuid, inference_uuid, user_reaction, user_comment, user):
        api_endpoint = "/feedback"
        url = get_url(self, api_endpoint)
        headers = get_headers(self.auth_token, json=True)
        payload = {
            "uuid": uuid,
            "inference_uuid": inference_uuid,
            "user": user,
            "user_reaction": 1 if user_reaction else 0,
            "user_comment": json.dumps(user_comment) if isinstance(user_comment, dict) else user_comment, 
        } 
        with httpx.Client() as client:
            response = client.put(url, headers=headers, json=payload)   
        return get_response(response, "Feedback")
