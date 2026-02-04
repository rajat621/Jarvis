import requests
import json
from typing import Iterator

LLAMA_API_URL = "http://localhost:11434/api/generate"

def query_llama(prompt: str) -> str:
    """
    Non-streaming call to the local LLaMA API.
    """
    response = requests.post(
        LLAMA_API_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "visible": False
        },
        timeout=30
    )
    try:
        return response.json().get("response", response.text)
    except ValueError:
        return response.text

def query_llama_stream(prompt: str) -> Iterator[str]:
    """
    Stream generator that yields partial responses from the LLaMA API.
    Expects the server to return one JSON object per line with a 'response' field.
    """
    response = requests.post(
        LLAMA_API_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "visible": False
        },
        stream=True,
        timeout=60
    )

    for line in response.iter_lines():
        if not line:
            continue
        try:
            payload = json.loads(line.decode())
        except json.JSONDecodeError:
            # ignore non-json lines
            continue
        if "response" in payload:
            yield payload["response"]
