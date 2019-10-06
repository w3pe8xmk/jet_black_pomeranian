# coding: UTF-8
from datetime import datetime
from discord.ext import tasks
import discord
import yaml
import random
import sys

f = open('settings.yml', 'r+')
data = yaml.load(f, Loader=yaml.SafeLoader)

TOKEN = data['TOKEN']   # 自分の Bot のアクセストークン
POMERANIAN_ID = data['POMERANIAN_ID']  # ポメラニアンのユーザーID

TSUCHINASHI_CHANNEL_ID = data['TSUCHINASHI_CHANNEL_ID']  # 通知なしチャンネル
GRABLUE_CHANNEL_ID = data['GRABLUE_CHANNEL_ID']  # グラブルチャンネル
HUKUDANCHO_CHANNEL_ID = data['HUKUDANCHO_CHANNEL_ID']  # 副団長とかチャンネル
PUBLICIZE_CHANNEL_ID = data['PUBLICIZE_CHANNEL_ID']  # 連絡用チャンネル

client = discord.Client()

@client.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時に動作する処理
# 現在受け取ったメッセージを elif で繋がって、新しいのを入れようとしたらどんどん下に増えていくので新しい関数とかでうまいこと処理されるようにしたい
@client.event
async def on_message(message):
    mentions = [x.id for x in message.mentions]
    if message.author.bot:
        return
    # リプライに反応する
    elif POMERANIAN_ID in mentions:
        if 'ハウス' in message.content:
            await message.channel.send('寝るポメ')
            await client.close()
            await sys.exit()
        else:
            msg = message.author.mention + ' ワン！(ちょっと何言ってるかわからないポメ)'
            await message.channel.send(msg)
    # 「ポメラニアン」に反応する
    elif 'ポメラニアン' in message.content:
        now = datetime.now().strftime('%S')
        if now == '01':
            await message.channel.send('キエエエェェェェーーーッ！！')
        else:
            await message.channel.send('ワン！')
    # 「ヒヒイロチャレンジ」に反応する
    elif 'ヒヒイロチャレンジ' in message.content:
        rand = random.randint(1, 1000)
        if rand <= 3:
            await message.channel.send('ヒヒイロカネが落ちたポメ！')
        elif rand >= 900:
            await message.channel.send('破局を受けたポメ！')
        else:
            await message.channel.send('オメガユニットしか落ちなかったポメ')
    # 「ルシ募集」に反応する
    elif message.content == 'ルシ募集':
        target_message = await message.channel.send('ダークラプチャー(HARD)の募集だポメ!\nやりたい属性のリアクションをするポメ')
        emoji_list = client.emojis
        # もっといい書き方あるかも
        for data in emoji_list:
            element_list = ['fire', 'water', 'earth', 'wind', 'light', 'dark']
            if data.name in element_list:
                await target_message.add_reaction(str(data))

# こうゆうのファイル分けたほうが良さそう?
# 定期発言(60秒に一回ループ)
# このやり方よくない、時間になったら実行されるようにしたい
# 古戦場期間中じゃなくても時間にあれば動いちゃうから、コメントアウトで退避
'''
@tasks.loop(seconds=60)
async def loop():
    now = datetime.now().strftime('%H:%M')

    if now == '00:00':
        channel = client.get_channel(GRABLUE_CHANNEL_ID)
        await channel.send('お疲れ様だポメ！')
        print(now)
    elif now == '07:00':
        channel = client.get_channel(PUBLICIZE_CHANNEL_ID)
        target_message = await channel.send('今日の相手に勝ちに行くポメ?')
        await target_message.add_reaction('👍')
        await target_message.add_reaction('👎')
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
'''
client.run(TOKEN)
