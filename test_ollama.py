import httpx
import os

def test_ollama():
    api_url = os.getenv('OLLAMA_API_URL', 'http://ollama:11434')
    api_key = os.getenv('OLLAMA_API_KEY', 'ollama')
    model = os.getenv('OLLAMA_MODEL', 'llama3.1')

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {api_key}" if api_key else "",
        "Content-Type": "application/json"
    }

    with httpx.Client() as client:
        response = client.post(f"{api_url}/v1/chat/completions", json=payload, headers=headers)
        print(response.json())

if __name__ == "__main__":
    test_ollama()
