# bot/utils/ollama.py

import httpx
import os
import logging

OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://ollama:11434')  # Docker service name

async def query_ollama(model: str, prompt: str) -> str:
    """
    Sends a prompt to the Ollama LLM and returns the response.

    :param model: The model name to use (e.g., 'llama').
    :param prompt: The prompt to send to the model.
    :return: The model's response as a string.
    """
    url = f"{OLLAMA_API_URL}/run/{model}"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'query': prompt
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers, timeout=60.0)
            response.raise_for_status()
            result = response.json()
            return result.get('response', '')
        except httpx.RequestError as e:
            logging.error(f"An error occurred while requesting Ollama: {e}")
            return "Sorry, I'm having trouble connecting to my brain right now."
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error while requesting Ollama: {e}")
            return "Sorry, something went wrong while processing your request."
        except Exception as e:
            logging.error(f"Unexpected error while requesting Ollama: {e}")
            return "Sorry, an unexpected error occurred."
