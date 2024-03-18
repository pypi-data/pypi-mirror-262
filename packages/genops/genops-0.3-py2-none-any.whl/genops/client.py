import requests
import json
import threading
import logging

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

        try:
            response = requests.post(endpoint_url, json=payload)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending submit request: {e}")
            raise
    
    def submit_async(self, prompt=None, response=None):
        if not prompt and not response:
            raise ValueError("At least one of 'prompt' or 'response' must be provided.")

        payload = {"project_key": self.project_key}
        if prompt:
            payload["prompt"] = prompt
        if response:
            payload["response"] = response

        protocol = "https" if self.use_https else "http"
        endpoint_url = f"{protocol}://{self.url}/api/projects/{self.project_id}/endpoints/{self.endpoint_id}"

        def send_request():
            try:
                response = requests.post(endpoint_url, json=payload)
                response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            except requests.exceptions.RequestException as e:
                logging.error(f"Error sending asynchronous request: {e}")

        threading.Thread(target=send_request).start()

def connect(url, project_id, endpoint_id, project_key, use_https=True):
    if not all(isinstance(arg, str) for arg in [url, project_id, endpoint_id, project_key]):
        raise TypeError("The 'url', 'project_id', 'endpoint_id', and 'project_key' arguments must be strings.")
    return GenOpsClient(url, project_id, endpoint_id, project_key, use_https)