# bot/cogs/user_settings.py

from nextcord.ext import commands
from bot.utils.database import get_db
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import logging


Base = declarative_base()

class UserSettings(Base):
    __tablename__ = 'user_settings'
    user_id = Column(Integer, primary_key=True, index=True)
    favorite_color = Column(String, nullable=True)

class UserSettingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info('UserSettings Cog initialized.')

    @commands.command(name='setcolor')
    async def set_color(self, ctx, color: str):
        """Sets the user's favorite color."""
        async for session in get_db():
            user = await session.get(UserSettings, ctx.author.id)
            if not user:
                user = UserSettings(user_id=ctx.author.id, favorite_color=color)
                session.add(user)
            else:
                user.favorite_color = color
            await session.commit()
            await ctx.send(f'{ctx.author.mention}, your favorite color has been set to {color}.')

    @commands.command(name='getcolor')
    async def get_color(self, ctx):
        """Gets the user's favorite color."""
        async for session in get_db():
            user = await session.get(UserSettings, ctx.author.id)
            if user and user.favorite_color:
                await ctx.send(f'{ctx.author.mention}, your favorite color is {user.favorite_color}.')
            else:
                await ctx.send(f'{ctx.author.mention}, you have not set a favorite color.')

def setup(bot):
    bot.add_cog(UserSettingsCog(bot))
