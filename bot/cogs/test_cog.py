# bot/cogs/test_cog.py

from nextcord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Responds with Pong!"""
        await ctx.send('Pong!')

def setup(bot):
    bot.add_cog(TestCog(bot))
