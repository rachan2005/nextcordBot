# bot/main.py

import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import logging

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
        
async def handle_health(request):
    return web.Response(text="Bot is running.")

app = web.Application()
app.add_routes([web.get('/health', handle_health)])

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            logging.info(f'Loaded extension {extension}')
        except Exception as e:
            logging.error(f'Failed to load extension {extension}.', exc_info=True)

    bot.run(TOKEN)
