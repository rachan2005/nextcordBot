# bot/main.py
import httpx
import os
import logging
import nextcord  # Import nextcord directly to access Intents
from nextcord.ext import commands
from dotenv import load_dotenv

# -------------------------------
# 1. Load Environment Variables
# -------------------------------

# Load environment variables from a .env file located in the same directory
load_dotenv()

# Retrieve the Discord bot token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Retrieve Ollama configurations from environment variables
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://ollama:11434')  # Default to Docker service name
OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')  # Optional, depending on your Ollama setup
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.1')  # Default model name

# PostgreSQL configurations (if used elsewhere in your bot)
DATABASE_URL = os.getenv('DATABASE_URL')

# Validate essential environment variables
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN is not set in the environment variables.")

# ----------------------------------
# 2. Configure Logging
# ----------------------------------

# Configure the logging module to display INFO level logs and above
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    handlers=[
        logging.StreamHandler()  # Log to stdout for Docker compatibility
    ]
)

# Create a logger instance for this module
logger = logging.getLogger('nextcord')

# ----------------------------------
# 3. Define Bot Intents
# ----------------------------------

# Define the intents your bot will use
intents = nextcord.Intents.default()
intents.message_content = True  # Essential for reading message content and commands

# Initialize the bot with a command prefix, defined intents, and disable the default help command
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# ----------------------------------
# 4. List of Extensions (Cogs)
# ----------------------------------

# Define a list of initial extensions (Cogs) to load
initial_extensions = [
    'bot.cogs.llm',             # Cog for LLM functionalities
    'bot.cogs.greetings',       # Cog for greeting commands
    'bot.cogs.user_settings',   # Cog for user settings commands
    'bot.cogs.test_cog',        # Cog for testing commands
    'bot.cogs.simple_cog',      # Cog for simple commands like !ping
    # Add additional Cogs here as needed
]

# ----------------------------------
# 5. Function to Load Extensions
# ----------------------------------

def load_extensions():
    """
    Load all Cogs/extensions listed in initial_extensions.
    Logs success or failure for each extension.
    """
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            logger.info(f"✅ Loaded extension '{extension}'")
        except commands.ExtensionAlreadyLoaded:
            logger.warning(f"⚠️ Extension '{extension}' is already loaded.")
        except commands.NoEntryPointError:
            logger.error(f"❌ Extension '{extension}' does not have a setup function.")
        except commands.ExtensionFailed as e:
            logger.error(f"❌ Extension '{extension}' failed to load. {e}")
        except Exception as e:
            logger.error(f"❌ An unexpected error occurred while loading extension '{extension}'.", exc_info=True)

# ----------------------------------
# 6. Bot Event Handlers
# ----------------------------------
@bot.event
async def on_ready():
    """
    Event handler for when the bot has successfully connected to Discord.
    Logs the bot's username and ID.
    """
    logger.info(f'🔗 Logged in as {bot.user} (ID: {bot.user.id})')
    logger.info('🚀 Bot is ready and operational!')

    # Load the model in Ollama
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{OLLAMA_API_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": ""
                },
                headers={
                    "Authorization": f"Bearer {OLLAMA_API_KEY}" if OLLAMA_API_KEY else "",
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()
            logger.info(f"✅ Model '{OLLAMA_MODEL}' loaded successfully in Ollama.")
        except Exception as e:
            logger.error(f"❌ Failed to load model '{OLLAMA_MODEL}' in Ollama: {e}")

@bot.event
async def on_ready():
    """
    Event handler for when the bot has successfully connected to Discord.
    Logs the bot's username and ID.
    """
    logger.info(f'🔗 Logged in as {bot.user} (ID: {bot.user.id})')
    logger.info('🚀 Bot is ready and operational!')

@bot.event
async def on_command_error(ctx, error):
    """
    Global error handler for commands.
    Handles common errors and logs unexpected ones.
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❓ Sorry, I didn't understand that command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Missing arguments for this command. Please check the command usage.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ You're on cooldown. Try again in {round(error.retry_after, 2)} seconds.")
    else:
        # For unexpected errors, log the exception and inform the user
        logger.error(f"⚠️ An error occurred: {error}", exc_info=True)
        await ctx.send("⚠️ An unexpected error occurred while processing your command.")

# ----------------------------------
# 7. Bot Commands (Custom Help)
# ----------------------------------

@bot.command(name='help')
async def help_command(ctx):
    """
    Sends a custom help message listing all available commands.
    """
    help_text = """
    **🤖 Available Commands:**
    - `!ping`: Check if the bot is responsive.
    - `!ask <question>`: Ask a question to the LLM.
    - `!summarize <text>`: Get a summary of the provided text.
    - `!setcolor <color>`: Set your favorite color.
    - `!getcolor`: Retrieve your favorite color.
    - `!settimezone <timezone>`: Set your timezone.
    - `!gettimezone`: Retrieve your timezone.
    - `!setlanguage <language>`: Set your preferred language.
    - `!getlanguage`: Retrieve your preferred language.
    - Add more commands as you expand your bot!
    """
    await ctx.send(help_text)

# ----------------------------------
# 8. Main Function to Run the Bot
# ----------------------------------

def main():
    """
    Main entry point for the bot.
    Loads extensions and starts the bot.
    """
    load_extensions()
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.critical("❌ Failed to start the bot.", exc_info=True)

# ----------------------------------
# 9. Execute Main Function
# ----------------------------------

if __name__ == '__main__':
    main()
