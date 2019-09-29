# coding: UTF-8
from datetime import datetime
from discord.ext import tasks
import discord
import yaml
import random

f = open('settings.yml', 'r+')
data = yaml.load(f, Loader = yaml.SafeLoader)

TOKEN = data['TOKEN']   # 自分の Bot のアクセストークン
POMERANIAN_ID = data['POMERANIAN_ID'] # ポメラニアンのユーザーID

TSUCHINASHI_CHANNEL_ID = data['TSUCHINASHI_CHANNEL_ID'] # 通知なしチャンネル
GRABLUE_CHANNEL_ID = data['GRABLUE_CHANNEL_ID'] # グラブルチャンネル
HUKUDANCHO_CHANNEL_ID = data['HUKUDANCHO_CHANNEL_ID'] # 副団長とかチャンネル
PUBLICIZE_CHANNEL_ID = data['PUBLICIZE_CHANNEL_ID'] # 連絡用チャンネル

client = discord.Client()

@client.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    mentions = [x.id for x in message.mentions]
    if message.author.bot:
        return
    # リプライに反応する
    elif POMERANIAN_ID in mentions:
        msg = message.author.mention + ' ワン！(ちょっと何言ってるかわからないポメ)'
        await message.channel.send(msg)
    # 「ポメラニアン」に反応する
    elif 'ポメラニアン' in message.content:
        now = datetime.now().strftime('%S')
        if now == '01':
            await message.channel.send('キエエエェェェェーーーッ！！')
        else:
            await message.channel.send('ワン！')
    elif 'ヒヒイロ' in message.content:
        rand=random.randint(1,1000)
        print(rand)
        if rand==1 or rand==2 or rand==3:
            await message.channel.send('ヒヒイロカネが落ちたポメ！')
        elif rand==15:
            await message.channel.send('破局を受けたポメ！')
        else:
            await message.channel.send('オメガユニットしか落ちなかったポメ')
        

        

# こうゆうのファイル分けたほうが良さそう?
# 定期発言(60秒に一回ループ)
# このやり方よくない、時間になったら実行されるようにしたい
@tasks.loop(seconds=60)
async def loop():
    now = datetime.now().strftime('%H:%M')

    if now == '00:00':
        channel = client.get_channel(GRABLUE_CHANNEL_ID)
        await channel.send('お疲れ様だポメ！')
        print(now)
    elif now == '07:00':
        channel = client.get_channel(PUBLICIZE_CHANNEL_ID)
        questionnaire_message = await channel.send('今日の相手に勝ちに行くポメ?')
        await questionnaire_message.add_reaction('👍')
        await questionnaire_message.add_reaction('👎')
        print(now)
    elif now == '19:59':
        channel = client.get_channel(GRABLUE_CHANNEL_ID)
        await channel.send('団サポ発動するポメ!')
        print(now)
    elif now == '21:00':
        # 「今日の相手に勝ちに行くポメ?」のリアクションによって発言を変えたい
        channel = client.get_channel(PUBLICIZE_CHANNEL_ID)
        await channel.send('アンケートの結果を見るポメ！')
        print(now)
loop.start()

client.run(TOKEN)
