
import random

import discord
from discord import app_commands
from discord.ext import commands


class HihiiroChallenge(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hihi", description="ヒヒイロカネチャレンジ")
    async def hihiiro(self, interaction: discord.Interaction):

        rand = random.randint(1, 100)

        if rand <= 3:
            response = 'ヒヒイロカネが落ちたポメ！'
        elif rand >= 90:
            response = '破局を受けたポメ！'
        else:
            response = 'オメガユニットしか落ちなかったポメ'

        await interaction.response.send_message(response)


async def setup(bot: commands.Bot):
    await bot.add_cog(HihiiroChallenge(bot))
