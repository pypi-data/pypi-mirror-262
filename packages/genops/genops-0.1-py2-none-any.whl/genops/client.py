import requests
import json

def connect(url, project_id, endpoint_id, project_key, use_https=True):
    protocol = "https" if use_https else "http"
    endpoint_url = f"{protocol}://{url}/api/projects/{project_id}/endpoints/{endpoint_id}"

    def submit(prompt, conversation_id=None):
        payload = {
            "prompt": prompt,
            "project_key": project_key,
        }
        if conversation_id:
            payload["conversation_id"] = conversation_id

        response = requests.post(endpoint_url, json=payload)
        return response.json()

    return submit