
import discord
from discord import app_commands
from discord.ext import commands


class BeelzebubHL(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="bub", description="ベルゼバブ募集")
    async def beelzebub(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "@here バブさんの募集だポメ！\n要望がなければ21時開始だポメ\n参加する討伐方法でリアクションするポメ！\n\U0001F1E6: 通常\n\U0001F1E7: システム\n\U0001F1E8: どちらも可"
        )
        message = await interaction.original_response()
        reaction_list = [
            '\U0001F1E6',  # A
            '\U0001F1E7',  # B
            '\U0001F1E8',  # C
        ]
        reactions = await self.bot.get_reactions(reaction_list)
        for reaction in reactions:
            await message.add_reaction(reaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(BeelzebubHL(bot))
