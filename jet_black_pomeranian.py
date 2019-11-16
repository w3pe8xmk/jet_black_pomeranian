# coding: UTF-8
from datetime import datetime, timedelta, timezone
from discord.ext import tasks
import discord
import random
import os
import subprocess
import yaml

f = open('unite_and_fight_schedule.yml', 'r+')
schedule = yaml.load(f, Loader=yaml.SafeLoader)

DISCORD_TOKEN = os.environ['DISCORD_TOKEN']   # 自分の Bot のアクセストークン
POMERANIAN_ID = os.environ['POMERANIAN_ID']  # ポメラニアンのユーザーID

TSUCHINASHI_CHANNEL_ID = os.environ['TSUCHINASHI_CHANNEL_ID']  # 通知なしチャンネル
GRABLUE_CHANNEL_ID = os.environ['GRABLUE_CHANNEL_ID']  # グラブルチャンネル
HUKUDANCHO_CHANNEL_ID = os.environ['HUKUDANCHO_CHANNEL_ID']  # 副団長とかチャンネル
PUBLICIZE_CHANNEL_ID = os.environ['PUBLICIZE_CHANNEL_ID']  # 連絡用チャンネル

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
        target_message = await message.channel.send('ダークラプチャー(HARD)の募集だポメ!\nできる属性(複数可)のリアクションをするポメ')
        emoji_list = client.emojis
        # もっといい書き方あるかも
        for data in emoji_list:
            element_list = ['fire', 'water', 'earth', 'wind', 'light', 'dark']
            if data.name in element_list:
                await target_message.add_reaction(str(data))

# こうゆうのファイル分けたほうが良さそう?
# 定期発言(60秒に一回ループ)
# このやり方よくない、時間になったら実行されるようにしたい
# とりあえず48回古戦場だけ対応、汎用的にしたい
@tasks.loop(seconds=60)
async def loop():
    JST = timezone(timedelta(hours=+9), 'JST')
    # now = datetime.now(JST).strftime('%Y/%m/%d %H:%M')
    now = datetime.now(JST)

    string_start_at = schedule[48]['start_at']
    string_end_at = schedule[48]['end_at']
    start_at = datetime.strptime(string_start_at, '%Y/%m/%d %z')
    end_at = datetime.strptime(string_end_at, '%Y/%m/%d %z')

    if start_at <= now <= end_at:
        now_time = now.strftime('%H:%M')
        if now_time == '00:00':
            channel = client.get_channel(GRABLUE_CHANNEL_ID)
            await channel.send('お疲れ様だポメ！')
        elif now_time == '19:59':
            channel = client.get_channel(GRABLUE_CHANNEL_ID)
            await channel.send('団サポ発動するポメ!')
        # 本戦
        if start_at + timedelta(days=3) <= now:
            if now_time == '07:00':
                channel = client.get_channel(PUBLICIZE_CHANNEL_ID)
                target_message = await channel.send('今日の相手に勝ちに行くポメ?')
                await target_message.add_reaction('👍')
                await target_message.add_reaction('👎')
            elif nonow_timew == '21:00':
                # 「今日の相手に勝ちに行くポメ?」のリアクションによって発言を変えたい
                channel = client.get_channel(PUBLICIZE_CHANNEL_ID)
                await channel.send('アンケートの結果を見るポメ！')
loop.start()

client.run(DISCORD_TOKEN)
