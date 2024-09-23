# bot/cogs/llm.py

import os
import httpx
import asyncio
from nextcord.ext import commands
from nextcord import Embed

class LLMCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = os.getenv('OLLAMA_API_URL', 'http://ollama:11434')
        self.api_key = os.getenv('OLLAMA_API_KEY')  # If Ollama requires an API key
        self.model = os.getenv('OLLAMA_MODEL', 'llama3.1')  # Ensure this matches the correct model name
        self.client = httpx.AsyncClient()

    def cog_unload(self):
        asyncio.create_task(self.client.aclose())

    @commands.command(name='ask')
    async def ask_llm(self, ctx, *, question: str):
        """Asks a question to the LLM."""
        await ctx.trigger_typing()
        try:
            response = await self.client.post(
                f"{self.api_url}/v1/completions",  # Corrected endpoint based on the API documentation
                json={
                    "model": self.model,
                    "prompt": question,
                    "max_tokens": 150,
                    "temperature": 0.7,
                    "stream": True  # Set to True if you want streaming responses
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()
            data = response.json()
            completion = data.get('response', 'No response.')
            await ctx.send(completion)
        except httpx.HTTPError as e:
            await ctx.send("Sorry, I couldn't process your request due to an HTTP error.")
            self.bot.logger.error(f"HTTP error occurred: {e}")
        except Exception as e:
            await ctx.send("⚠️ An unexpected error occurred while processing your command.")
            self.bot.logger.error(f"Unexpected error: {e}", exc_info=True)

    @commands.command(name='summarize')
    async def summarize_llm(self, ctx, *, text: str):
        """Summarizes the provided text using the LLM."""
        await ctx.trigger_typing()
        try:
            prompt = f"Summarize the following text:\n{text}"
            response = await self.client.post(
                f"{self.api_url}/v1/completions",  # Corrected endpoint based on the API documentation
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "max_tokens": 150,
                    "temperature": 0.5,
                    "stream": False  # Set to True if you want streaming responses
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()
            data = response.json()
            summary = data.get('response', 'No summary available.')
            await ctx.send(summary)
        except httpx.HTTPError as e:
            await ctx.send("Sorry, I couldn't process your request due to an HTTP error.")
            self.bot.logger.error(f"HTTP error occurred: {e}")
        except Exception as e:
            await ctx.send("⚠️ An unexpected error occurred while processing your command.")
            self.bot.logger.error(f"Unexpected error: {e}", exc_info=True)

def setup(bot):
    bot.add_cog(LLMCog(bot))
