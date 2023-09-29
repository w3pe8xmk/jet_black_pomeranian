
import discord
from discord import app_commands
from discord.ext import commands


class SuperUltimateBahamut(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='spbh', description='スパバハ募集')
    async def super_ultimate_bahamut(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            'スパバハ参加者を募集します。参加する属性を選んでください。'
        )
        message = await interaction.original_response()
        reaction_list = [
            'hai'
        ]
        reactions = await self.bot.get_reactions(reaction_list)
        for reaction in reactions:
            await message.add_reaction(reaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(SuperUltimateBahamut(bot))
