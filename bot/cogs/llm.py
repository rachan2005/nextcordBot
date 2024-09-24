# bot/cogs/llm.py

import os
import httpx
import asyncio
import json
from nextcord.ext import commands
from nextcord import Embed
import logging

# Create a logger for the cog
logger = logging.getLogger(__name__)

class LLMCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = os.getenv('OLLAMA_API_URL', 'http://ollama:11434')
        self.api_key = os.getenv('OLLAMA_API_KEY')  # If Ollama requires an API key
        self.model = os.getenv('OLLAMA_MODEL', 'llama3.1')  # Ensure this matches the model name
        self.client = httpx.AsyncClient()

    def cog_unload(self):
        asyncio.create_task(self.client.aclose())

    @commands.command(name='ask')
    async def ask_llm(self, ctx, *, question: str):
        """Asks a question to the LLM."""
        await ctx.trigger_typing()
        try:
            payload = {
                "model": self.model,
                "prompt": question,
                "max_tokens": 10000,  # Increase max_tokens if necessary
                "temperature": 0.7,
                "stream": False
            }
            logger.info(f"Sending request to Ollama API: {json.dumps(payload)}")
            response = await self.client.post(
                f"{self.api_url}/api/generate",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                    "Content-Type": "application/json"
                }
            )
            logger.info(f"Received response from Ollama API: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response JSON: {json.dumps(data)}")
            completion = data.get('response', 'No response.')
            # Split the response if it's longer than 2000 characters
            if len(completion) > 350:
                chunks = [completion[i:i+350] for i in range(0, len(completion), 350)]
                for chunk in chunks:
                    await ctx.send(chunk)
                    await asyncio.sleep(3)
            else:
                await ctx.send(completion)
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP status error: {e.response.status_code} - {e.response.text}")
            await ctx.send("Sorry, I couldn't process your request due to an HTTP error.")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            await ctx.send("Sorry, I couldn't process your request due to a network error.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            await ctx.send("⚠️ An unexpected error occurred while processing your command.")

    @commands.command(name='summarize')
    async def summarize_llm(self, ctx, *, text: str):
        """Summarizes the provided text using the LLM."""
        await ctx.trigger_typing()
        try:
            prompt = f"Summarize the following text:\n{text}"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "max_tokens": 1500,  # Increase max_tokens if necessary
                "temperature": 0.5,
                "stream": False
            }
            logger.info(f"Sending summarize request to Ollama API: {json.dumps(payload)}")
            response = await self.client.post(
                f"{self.api_url}/api/generate",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                    "Content-Type": "application/json"
                }
            )
            logger.info(f"Received response from Ollama API: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Response JSON: {json.dumps(data)}")
            summary = data.get('response', 'No summary available.')
            # Split the summary if it's longer than 2000 characters
            if len(summary) > 2000:
                chunks = [summary[i:i+2000] for i in range(0, len(summary), 2000)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(summary)
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP status error: {e.response.status_code} - {e.response.text}")
            await ctx.send("Sorry, I couldn't process your request due to an HTTP error.")
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            await ctx.send("Sorry, I couldn't process your request due to a network error.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            await ctx.send("⚠️ An unexpected error occurred while processing your command.")

def setup(bot):
    bot.add_cog(LLMCog(bot))
