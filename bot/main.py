# bot/main.py

import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import logging
import sys
import signal
import asyncio

from bot.utils.database import engine
from bot.models.user_settings import Base  # Import your models here

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Retrieve the bot token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = nextcord.Intents.default()
intents.message_content = True  # Enable if your bot needs to read message content

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
initial_extensions = [
    'bot.cogs.example_cog',
    'bot.cogs.greetings',
    'bot.cogs.user_settings',
    'bot.cogs.llm',  # Newly added LLM cog
    # Add other cogs here
]

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info('------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I didn't understand that command.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required permissions to use this command.")
    else:
        logging.error(f'Unhandled exception: {error}', exc_info=True)
        await ctx.send("An error occurred while processing the command.")

if __name__ == '__main__':
    async def init_db():
        async with engine.begin() as conn:
            # Import all models here
            await conn.run_sync(Base.metadata.create_all)
        logging.info("Database initialized.")

    async def load_extensions():
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
                logging.info(f'Loaded extension {extension}')
            except Exception as e:
                logging.error(f'Failed to load extension {extension}.', exc_info=True)


    async def shutdown(signal, frame):
        logging.info("Shutting down bot...")
        await bot.close()
        sys.exit(0)

    # Register signal handlers for graceful shutdown
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown(s, None)))

    async def main():
        await init_db()
        load_extensions()
        try:
            await bot.start(TOKEN)
        except nextcord.LoginFailure:
            logging.error("Invalid Discord token.")
        except Exception as e:
            logging.error("An unexpected error occurred.", exc_info=True)


    loop.run_until_complete(main())
