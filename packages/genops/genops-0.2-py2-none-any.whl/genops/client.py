import requests
import json

class GenOpsClient:
    def __init__(self, url, project_id, endpoint_id, project_key, use_https=True):
        self.url = url
        self.project_id = project_id
        self.endpoint_id = endpoint_id
        self.project_key = project_key
        self.use_https = use_https

    def submit(self, prompt, conversation_id=None):
        protocol = "https" if self.use_https else "http"
        endpoint_url = f"{protocol}://{self.url}/api/projects/{self.project_id}/endpoints/{self.endpoint_id}"

        payload = {
            "prompt": prompt,
            "project_key": self.project_key,
        }
        if conversation_id:
            payload["conversation_id"] = conversation_id

        response = requests.post(endpoint_url, json=payload)
        return response.json()

def connect(url, project_id, endpoint_id, project_key, use_https=True):
    if not all(isinstance(arg, str) for arg in [url, project_id, endpoint_id, project_key]):
        raise TypeError("The 'url', 'project_id', 'endpoint_id', and 'project_key' arguments must be strings.")
    return GenOpsClient(url, project_id, endpoint_id, project_key, use_https)