# coding: UTF-8
import asyncio
import os

import discord
from discord.ext import commands
import yaml
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# 自分の Bot のアクセストークン
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
# ポメラニアンのユーザーID
POMERANIAN_ID = os.environ['POMERANIAN_ID']
# メインテキストチャンネル
GRABLUE_CHANNEL_ID = os.environ['GRABLUE_CHANNEL_ID']
# 連絡用チャンネル
PUBLICIZE_CHANNEL_ID = os.environ['PUBLICIZE_CHANNEL_ID']
# マルチ募集チャンネル
RECRUITMENT_CHANNEL_ID = os.environ['RECRUITMENT_CHANNEL_ID']
# スプレッドシートのURL
GSPREAD_URL = os.environ['GSPREAD_URL']

# TODO:将来的にIntentは最低限にしたい
intents = discord.Intents.all()
#intents = discord.Intents.default()
intents.typing = False


class JetBrackPomeranian(commands.Bot):
    """JetBlackPomeranianボット本体

    Args:
        commands (_type_): _description_
    """

    def __init__(self):
        super().__init__(
            command_prefix='/',
            intents=intents
        )

        self.INITIAL_EXTENSIONS = [
            'cogs.battle.proto_bahamut_hl',
            'cogs.battle.ultimate_bahamut_hl',
            'cogs.battle.lucifer_hl',
            'cogs.battle.beelzebub_hl',
            'cogs.battle.belial_hl',
            'cogs.battle.super_ultimate_bahamut',
            'cogs.hobby.hihiiro_challenge',
            'cogs.hobby.pomeranian',
            'cogs.schedule.minute_schedule',
        ]

        # 古戦場とドレバラのスケジュール
        schedule_file = open('schedule.yml', 'r+')
        self.schedule = yaml.load(schedule_file, Loader=yaml.SafeLoader)

        # スプレッドシートのURL
        self.GSPREAD_URL = os.environ['GSPREAD_URL']

    async def on_ready(self):
        print('ログインしました')

    async def setup_hook(self):
        await self.setup_botinit()
        await self.load_cogs(self.INITIAL_EXTENSIONS)
        await self.tree.sync()

    async def load_cogs(self, extensions):
        for extension in extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(f'{extension}の読み込みでエラー発生 {e}')

    async def setup_botinit(self):
        self.grablue_channel = await self.fetch_channel(int(GRABLUE_CHANNEL_ID))
        self.publicize_channel = await self.fetch_channel(int(PUBLICIZE_CHANNEL_ID))
        self.recruitment_channel = await self.fetch_channel(int(RECRUITMENT_CHANNEL_ID))

    async def close(self):
        await super().close()

    async def get_reactions(self, reaction_list):
        """リアクション取得

        Args:
            reaction_list (_type_): リアクションの文字配列

        Returns:
            _type_: Discordが認識するリアクション
        """
        emoji_list = self.emojis
        emoji_hash = {emoji.name: emoji for emoji in emoji_list}
        results = []
        for reaction in reaction_list:
            if reaction in emoji_hash.keys():
                results.append(str(emoji_hash[reaction]))
            else:
                results.append(reaction)
        return results


bot = JetBrackPomeranian()
bot.run(DISCORD_TOKEN)
