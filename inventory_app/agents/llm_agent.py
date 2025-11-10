import requests
from django.conf import settings

def recommend_reorders(summary_payload):
    endpoint = settings.LLM_ENDPOINT
    headers = {"Authorization": f"Bearer {settings.LLM_API_KEY}"}
    prompt = {"prompt": f"Sugiere reordenes: {summary_payload}"}
    response = requests.post(endpoint, json=prompt, headers=headers)
    return response.json()