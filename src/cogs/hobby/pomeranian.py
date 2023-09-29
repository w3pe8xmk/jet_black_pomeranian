
import datetime

import discord
from discord import app_commands
from discord.ext import commands


class Pomeranian(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="pome", description="ヒヒイロカネチャレンジ")
    async def pomeranian(self, interaction: discord.Interaction):

        now = datetime.now().strftime('%S')
        response = 'キエエエェェェェーーーッ！！' if now == '01' else 'ワン！'

        await interaction.response.send_message(response)


async def setup(bot: commands.Bot):
    await bot.add_cog(Pomeranian(bot))
