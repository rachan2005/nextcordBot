from nextcord.ext import commands
import logging

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info('ExampleCog initialized.')

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Responds with Pong!"""
        await ctx.send('Pong!')

def setup(bot):
    bot.add_cog(ExampleCog(bot))
