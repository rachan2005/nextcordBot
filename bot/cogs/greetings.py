from nextcord.ext import commands
import logging

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info('Greetings Cog initialized.')

    @commands.command(name='hello')
    async def hello(self, ctx):
        """Says hello to the user."""
        await ctx.send(f'Hello, {ctx.author.mention}!')

def setup(bot):
    bot.add_cog(Greetings(bot))
