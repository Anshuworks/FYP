"""
Qwen/Ollama Client

A reusable, dependency-free client for calling a local Ollama instance.
Uses only Python standard library (urllib, json).

This client is model-agnostic — it sends a prompt and returns the raw
text response. Extraction logic lives in extractor.py.
"""
import json
import urllib.request
import urllib.error
from typing import Optional


# Default Ollama endpoint
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen3:1.7b"

# Request timeout in seconds
DEFAULT_TIMEOUT = 120


class QwenClientError(Exception):
    """Raised when the Ollama API call fails."""
    pass


def generate(
    prompt: str,
    model: str = DEFAULT_MODEL,
    ollama_url: str = DEFAULT_OLLAMA_URL,
    timeout: int = DEFAULT_TIMEOUT,
    temperature: float = 0.1,
    system: Optional[str] = None,
) -> str:
    """
    Sends a prompt to a local Ollama instance and returns the response text.

    Args:
        prompt:     The user prompt to send.
        model:      The Ollama model name (default: 'qwen3:4b').
        ollama_url: The Ollama API endpoint URL.
        timeout:    Request timeout in seconds.
        temperature: Sampling temperature. Low values (0.1) for deterministic
                     extraction; higher values for creative tasks.
        system:     Optional system prompt to set the model's behavior.

    Returns:
        The model's response text as a string.

    Raises:
        QwenClientError: If the request fails, times out, or the response
                         cannot be parsed.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {
            "temperature": temperature,
        },
    }

    if system is not None:
        payload["system"] = system

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        ollama_url,
        data=data,
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        raise QwenClientError(
            f"Failed to connect to Ollama at {ollama_url}: {e}"
        ) from e
    except TimeoutError as e:
        raise QwenClientError(
            f"Ollama request timed out after {timeout}s: {e}"
        ) from e

    try:
        result = json.loads(body)
    except json.JSONDecodeError as e:
        raise QwenClientError(
            f"Ollama returned invalid JSON: {e}\nRaw response: {body[:500]}"
        ) from e

    if "response" not in result:
        raise QwenClientError(
            f"Ollama response missing 'response' field. Keys: {list(result.keys())}"
        )

    return result["response"]
