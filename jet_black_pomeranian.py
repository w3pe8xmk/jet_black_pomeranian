# coding: UTF-8
import os
import random
import subprocess
from datetime import datetime, timedelta, timezone

import discord
import yaml
from discord.ext import tasks

schedule_file = open('unite_and_fight_schedule.yml', 'r+')
schedule = yaml.load(schedule_file, Loader=yaml.SafeLoader)
# 自分の Bot のアクセストークン
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
# ポメラニアンのユーザーID
POMERANIAN_ID = os.environ['POMERANIAN_ID']
# 通知なしチャンネル
TSUCHINASHI_CHANNEL_ID = os.environ['TSUCHINASHI_CHANNEL_ID']
# グラブルチャンネル
GRABLUE_CHANNEL_ID = os.environ['GRABLUE_CHANNEL_ID']
# 副団長とかチャンネル
HUKUDANCHO_CHANNEL_ID = os.environ['HUKUDANCHO_CHANNEL_ID']
# 連絡用チャンネル
PUBLICIZE_CHANNEL_ID = os.environ['PUBLICIZE_CHANNEL_ID']
# マルチ募集チャンネル
RECRUITMENT_CHANNEL_ID = os.environ['RECRUITMENT_CHANNEL_ID']
# スプレッドシートのURL
GSPREAD_URL = os.environ['GSPREAD_URL']

CLIENT = discord.Client()
JST = timezone(timedelta(hours=+9), 'JST')


@CLIENT.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時に動作する処理
# TODO: クラスに分ける
@CLIENT.event
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
        rand = random.randint(1, 100)
        if rand <= 3:
            await message.channel.send('ヒヒイロカネが落ちたポメ！')
        elif rand >= 90:
            await message.channel.send('破局を受けたポメ！')
        else:
            await message.channel.send('オメガユニットしか落ちなかったポメ')
    # 「ルシ募集」に反応する
    elif message.content == 'ルシ募集':
        await lucifer(message.channel)
    # 「つよ募集」に反応する
    elif message.content == 'つよ募集':
        await tuyo(message.channel)

# 定期発言(60秒に一回ループ)
# TODO: このやり方よくない、時間になったら実行されるようにしたい
@tasks.loop(seconds=60)
async def loop():
    # TODO: 毎回変数に入れているからインスタンス変数か外に出したい
    grablue_channel = CLIENT.get_channel(int(GRABLUE_CHANNEL_ID))
    publicize_channel = CLIENT.get_channel(int(PUBLICIZE_CHANNEL_ID))
    recruitment_channel = CLIENT.get_channel(int(RECRUITMENT_CHANNEL_ID))

    now = datetime.now(JST).replace(second=0, microsecond=0)

    # TODO: とりあえず53回古戦場だけ対応、汎用的にしたい
    start_at_str = schedule[54]['start_at']
    end_at_str = schedule[54]['end_at']
    start_at = datetime.strptime(start_at_str, '%Y/%m/%d %z')
    end_at = datetime.strptime(end_at_str, '%Y/%m/%d %z')

    # 古戦場三日前
    if start_at - timedelta(days=3) == now:
        await grablue_channel.send('古戦場3日前だポメ、次回古戦場シートに一言と目標を記入するポメ！\n' + GSPREAD_URL)
    # 古戦場期間中
    now_time_str = now.strftime('%H:%M')
    if start_at < now < end_at:
        # 予選開始時
        if start_at + timedelta(hours=19) == now:
            await grablue_channel.send('古戦場予選開始ポメ。応援してるポメ！')
        # 古戦場、毎日
        if now_time_str == '00:00':
            await grablue_channel.send('お疲れ様ポメ！')
        elif now_time_str == '19:59':
            await grablue_channel.send('団アビ発動するポメ!')
        elif now_time_str == '21:59':
            await grablue_channel.send('2回目の団アビ発動し忘れてないポメ？')
        # 予選終了時
        if start_at + timedelta(days=2) == now:
            await grablue_channel.send('予選お疲れ様ポメ！明日はインターバルだポメ')
        # 本戦開始日
        if start_at + timedelta(days=3) == now:
            await grablue_channel.send('7:00から本戦だポメ、明日に備えて寝るポメ！')
        # 本戦時、毎日
        if start_at + timedelta(days=3) <= now:
            if now_time_str == '07:00':
                target_message = await publicize_channel.send('今日の相手に勝ちに行くかと、現在の肉の個数をシートに記入するポメ!\n' + GSPREAD_URL + '\n14時時点で15人以上「勝ちに行く」なら勝ちにいく方針になるポメ\n忙しくて走れないと分かってる日は事前にその日を△にしとくといいポメ')
            elif now_time_str == '14:00':
                # シートのAPIで勝ちに行くの個数を取得してその結果によって発言を変えたい
                channel = CLIENT.get_channel(PUBLICIZE_CHANNEL_ID)
                await publicize_channel.send(GSPREAD_URL + '\nアンケートの結果を見るポメ！15人以上「勝ちに行く」なら勝ちにいくポメ！')
    # 古戦場最終日
    elif end_at == now:
        await grablue_channel.send('本戦お疲れ様だポメ！明日はスペシャルバトルだポメ')

    # 古戦場期間外の定期
    elif now_time_str == '12:00':
        # ルシHard、土曜日のみ
        # TODO: マジックナンバーを避ける
        if now.weekday() == 5:
            await lucifer(recruitment_channel)
        # アルバハHL
        al_target_message = await recruitment_channel.send('アルバハHLの募集だポメ！\nリアクションした人から優先だポメ\n要望がなければ22時開始だポメ\n2部やる場合は別のリアクションをするポメ')
        await add_hai_reaction(al_target_message)
loop.start()


async def lucifer(channel):
    """ ルシファーの募集をチャンネルに投げる
    """
    target_message = await channel.send('ダークラプチャー(HARD)の募集だポメ!\nやりたい属性にリアクションをするポメ\nやりたい人いれば手伝うくらいの人は別のリアクション押すポメ！\n要望がなければ21時開始だポメ')
    emoji_list = CLIENT.emojis
    for data in emoji_list:
        reaction_list = [
            'fire',
            'water',
            'earth',
            'wind',
            'light',
            'dark',
            'narumea
        ]
        if data.name in reaction_list:
            await target_message.add_reaction(str(data))


async def tuyo(channel):
    """ つよバハの募集をチャンネルに投げる
    """
    tuyo_target_message = await channel.send('つよバハの募集だポメ！\n1部屋6人で自発者はサポでやるポメ\n要望がなければ21時開始だポメ')
    await add_hai_reaction(tuyo_target_message)


# TODO: ルシファーの方でも同じことしているからadd_reaction(message, stamp_names) みたいな感じに変えたい
async def add_hai_reaction(message):
    emoji_list = CLIENT.emojis
    for data in emoji_list:
        reaction_list = ['hai']
        if data.name in reaction_list:
            await message.add_reaction(str(data))

CLIENT.run(DISCORD_TOKEN)
