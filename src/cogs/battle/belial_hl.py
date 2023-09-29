
import discord
from discord import app_commands
from discord.ext import commands


class BelialHL(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="beli", description="ベリアル募集")
    async def belial(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "@here ベリアルの募集だポメ！\n要望がなければ21時開始だポメ"
        )
        message = await interaction.original_response()
        reaction_list = [
            'hai'
        ]
        reactions = await self.bot.get_reactions(reaction_list)
        for reaction in reactions:
            await message.add_reaction(reaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(BelialHL(bot))
