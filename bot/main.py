# bot/main.py

import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import logging
from config.config import DISCORD_TOKEN as TOKEN


# Configure logging
logging.basicConfig(level=logging.INFO)


# Define intents
intents = nextcord.Intents.default()
intents.message_content = True  # Enable if your bot needs to read message content

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
initial_extensions = [
    'bot.cogs.example_cog',
    'bot.cogs.greetings',
    # Add other cogs here
]

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            logging.info(f'Loaded extension {extension}')
        except Exception as e:
            logging.error(f'Failed to load extension {extension}.', exc_info=True)

    # Run the bot
    bot.run(TOKEN)
