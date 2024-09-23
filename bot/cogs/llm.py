# bot/cogs/llm.py

from nextcord.ext import commands
import httpx
import os
from dotenv import load_dotenv
import logging

load_dotenv()

class LLM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = os.getenv('OLLAMA_API_URL', 'http://ollama:11434')  # Use Docker service name for internal communication
        self.api_key = os.getenv('OLLAMA_API_KEY', None)
        self.model = os.getenv('OLLAMA_MODEL', 'llama3.1')  # Default model
        
        if not self.api_key:
            logging.warning("OLLAMA_API_KEY is not set. Proceeding without authentication.")
        logging.info('LLM Cog initialized.')

    @commands.command(name='ask')
    async def ask_llm(self, ctx, *, question: str):
        """Asks a question to the LLM and returns the response."""
        await ctx.trigger_typing()
        try:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'

            payload = {
                "prompt": question,
                "max_tokens": 150,
                "temperature": 0.7
                # Add other parameters as required by Ollama's API
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/v1/engines/{self.model}/completions",
                    json=payload,
                    headers=headers,
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                answer = data.get('response', 'No response from LLM.')
                await ctx.send(answer)
        except httpx.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            await ctx.send("Sorry, I couldn't process your request due to an HTTP error.")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
            await ctx.send("Sorry, something went wrong while processing your request.")

    @commands.command(name='summarize')
    async def summarize_llm(self, ctx, *, text: str):
        """Summarizes the provided text using the LLM."""
        await ctx.trigger_typing()
        try:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'

            prompt = f"Summarize the following text:\n\n{text}"

            payload = {
                "prompt": prompt,
                "max_tokens": 100,
                "temperature": 0.5
                # Adjust parameters as needed
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/v1/engines/{self.model}/completions",
                    json=payload,
                    headers=headers,
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                summary = data.get('response', 'No summary available.')
                await ctx.send(summary)
        except httpx.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            await ctx.send("Sorry, I couldn't process your request due to an HTTP error.")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
            await ctx.send("Sorry, something went wrong while processing your request.")

def setup(bot):
    bot.add_cog(LLM(bot))
