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

DISCORD_TOKEN = os.environ['DISCORD_TOKEN'] # 自分の Bot のアクセストークン
POMERANIAN_ID = os.environ['POMERANIAN_ID'] # ポメラニアンのユーザーID

TSUCHINASHI_CHANNEL_ID = os.environ['TSUCHINASHI_CHANNEL_ID'] # 通知なしチャンネル
GRABLUE_CHANNEL_ID = os.environ['GRABLUE_CHANNEL_ID'] # グラブルチャンネル
HUKUDANCHO_CHANNEL_ID = os.environ['HUKUDANCHO_CHANNEL_ID'] # 副団長とかチャンネル
PUBLICIZE_CHANNEL_ID = os.environ['PUBLICIZE_CHANNEL_ID'] # 連絡用チャンネル
RECRUITMENT_CHANNEL_ID = os.environ['RECRUITMENT_CHANNEL_ID'] # マルチ募集チャンネル

client = discord.Client()

JST = timezone(timedelta(hours=+9), 'JST')

@client.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時に動作する処理
# TODO: 現在受け取ったメッセージを elif で繋がって、新しいのを入れようとしたらどんどん下に増えていくので新しい関数とかでうまいこと処理されるようにしたい
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
        await lucifer(message.channel)

# TODO: こうゆうのファイル分けたほうが良さそう?
# 定期発言(60秒に一回ループ)
# TODO: このやり方よくない、時間になったら実行されるようにしたい
@tasks.loop(seconds=60)
async def loop():
    # TODO: 毎回変数に入れているからインスタンス変数か外に出したい
    grablue_channel = client.get_channel(int(GRABLUE_CHANNEL_ID))
    publicize_channel = client.get_channel(int(PUBLICIZE_CHANNEL_ID))
    recruitment_channel = client.get_channel(int(RECRUITMENT_CHANNEL_ID))

    now = datetime.now(JST)

    # TODO: とりあえず49回古戦場だけ対応、汎用的にしたい
    string_start_at = schedule[49]['start_at']
    string_end_at = schedule[49]['end_at']
    start_at = datetime.strptime(string_start_at, '%Y/%m/%d %z')
    end_at = datetime.strptime(string_end_at, '%Y/%m/%d %z')

    # FIXME: 古戦場三日前動いていないっぽい
    # 古戦場三日前
    if start_at - timedelta(days=3) == now:
        await grablue_channel.send('古戦場3日前だポメ、シート未記入なら記入するポメ！')
    # 古戦場期間中
    now_time = now.strftime('%H:%M')
    if start_at <= now < end_at:
        # 予選開始時
        if start_at + timedelta(hours=19) == now:
            await grablue_channel.send('古戦場予選開始だポメ。応援してるポメ！')
        # 古戦場、毎日
        if now_time == '00:00':
            await grablue_channel.send('お疲れ様だポメ！')
        elif now_time == '19:59':
            await grablue_channel.send('団アビ発動するポメ!')
        elif now_time == '21:59':
            await grablue_channel.send('2回目の団アビ発動し忘れてないポメ？')
        # 予選終了時
        if start_at + timedelta(days=2) == now:
            await grablue_channel.send('予選お疲れ様だポメ！明日はインターバルだポメ')
        # 本戦時、毎日
        if start_at + timedelta(days=3) <= now:
            if now_time == '07:00':
                target_message = await publicize_channel.send('今日の相手に勝ちに行くポメ? 😷は放棄の意味だポメ')
                await target_message.add_reaction('👍')
                await target_message.add_reaction('👎')
                await target_message.add_reaction('😷')
            elif now_time == '12:00':
                # 「今日の相手に勝ちに行くポメ?」のリアクションによって発言を変えたい
                channel = client.get_channel(PUBLICIZE_CHANNEL_ID)
                await publicize_channel.send('アンケートの結果を見るポメ！15人以上👍なら勝ちにいくポメ！')
    # 古戦場最終日
    elif end_at == now:
        await grablue_channel.send('本戦お疲れ様だポメ！明日はスペシャルバトルだポメ')
    # 古戦場期間外の定期
    elif now_time == '12:00':
        # ルシHard
        if now.weekday() == 5:
            await lucifer(recruitment_channel)
        # アルバハHL
        else:
            target_message = await recruitment_channel.send("アルバハHLの募集だポメ！\n参加する人はリアクションをするポメ\n要望がなければ23時開始だポメ")
            emoji_list = client.emojis
            # TODO: もっといい書き方あるかも、共通化する
            for data in emoji_list:
                element_list = ['hai']
                if data.name in element_list:
                    await target_message.add_reaction(str(data))
loop.start()

async def lucifer(channel):
    target_message = await channel.send('ダークラプチャー(HARD)の募集だポメ!\nできる属性(複数可)のリアクションをするポメ\n要望がなければ21時開始だポメ')
    emoji_list = client.emojis
    for data in emoji_list:
        element_list = ['fire', 'water', 'earth', 'wind', 'light', 'dark']
        if data.name in element_list:
            await target_message.add_reaction(str(data))

client.run(DISCORD_TOKEN)
