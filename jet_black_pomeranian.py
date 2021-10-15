# coding: UTF-8
import os
import random
from datetime import datetime, timedelta, timezone

import discord
import yaml
from discord.ext import tasks

# 古戦場とドレバラのスケジュール
schedule_file = open('schedule.yml', 'r+')
schedule = yaml.load(schedule_file, Loader=yaml.SafeLoader)
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

CLIENT = discord.Client()
JST = timezone(timedelta(hours=+9), 'JST')
CHANNELS = {}


@CLIENT.event
async def on_ready():
    """ 起動時
    """
    print('ログインしました')
    CHANNELS.update({
        'grablue_channel': CLIENT.get_channel(int(GRABLUE_CHANNEL_ID)),
        'publicize_channel': CLIENT.get_channel(int(PUBLICIZE_CHANNEL_ID)),
        'recruitment_channel': CLIENT.get_channel(int(RECRUITMENT_CHANNEL_ID))
    })
    loop.start()

# TODO: クラスに分ける
@CLIENT.event
async def on_message(message):
    """ メッセージ受信時に動作する処理
    """
    # bot からのメッセージは無視
    if message.author.bot:
        return
    # リプライに反応する
    mentions = [x.id for x in message.mentions]
    if POMERANIAN_ID in mentions:
        msg = message.author.mention + ' ワン！(ちょっと何言ってるかわからないポメ)'
        await message.channel.send(msg)
    # 「ポメラニアン」に反応する
    elif 'ポメラニアン' in message.content:
        now = datetime.now().strftime('%S')
        send_message = 'キエエエェェェェーーーッ！！' if now == '01' else 'ワン！'
        await message.channel.send(send_message)
    # 「ヒヒイロチャレンジ」に反応する
    elif 'ヒヒイロチャレンジ' in message.content:
        rand = random.randint(1, 100)
        if rand <= 3:
            await message.channel.send('ヒヒイロカネが落ちたポメ！')
        elif rand >= 90:
            await message.channel.send('破局を受けたポメ！')
        else:
            await message.channel.send('オメガユニットしか落ちなかったポメ')

    # 「アルバハ募集」に反応する
    elif message.content == 'アルバハ募集':
        await ultimate_bahamut(message.channel)
    # 「つよ募集」に反応する
    elif message.content == 'つよ募集':
        await proto_bahamut(message.channel)
    # 「ルシ募集」に反応する
    elif message.content == 'ルシ募集':
        await lucifer(message.channel)
    # 「バブ募集」に反応する
    elif message.content == 'バブ募集':
        await beelzebub(message.channel)
    # 「ベリアル募集」に反応する
    elif message.content == 'ベリアル募集':
        await belial(message.channel)

# TODO: このやり方よくない、時間になったら実行されるようにしたい
@tasks.loop(seconds=60)
async def loop():
    """ 定期発言(60秒に一回ループ)
    """
    grablue_channel = CHANNELS['grablue_channel']
    publicize_channel = CHANNELS['publicize_channel']
    recruitment_channel = CHANNELS['recruitment_channel']

    now = datetime.now(JST).replace(second=0, microsecond=0)
    now_time_str = now.strftime('%H:%M')

    # 古戦場のスケジュール
    unite_and_fight_schedule = schedule['unite_and_fight']
    max_unite_and_fight_schedule = max(unite_and_fight_schedule.items())[1]
    unite_and_fight_start_at = datetime.strptime(max_unite_and_fight_schedule['start_at'], '%Y/%m/%d %z')
    unite_and_fight_end_at = datetime.strptime(max_unite_and_fight_schedule['end_at'], '%Y/%m/%d %z')
    # ドレバラのスケジュール
    team_force_schedule = schedule['team_force']
    max_team_force_schedule = max(team_force_schedule.items())[1]
    team_force_start_at = datetime.strptime(max_team_force_schedule['start_at'], '%Y/%m/%d %z')
    team_force_end_at = datetime.strptime(max_team_force_schedule['end_at'], '%Y/%m/%d %z')

    # 古戦場1日前
    if unite_and_fight_start_at - timedelta(hours=5) == now:
        await grablue_channel.send('明日から古戦場だポメ、次回古戦場シートに一言と目標を記入するポメ！\n' + GSPREAD_URL)
    # 古戦場期間中
    if unite_and_fight_start_at < now < unite_and_fight_end_at:
        # 予選開始時
        if unite_and_fight_start_at + timedelta(hours=19) == now:
            await grablue_channel.send('古戦場予選開始ポメ。応援してるポメ！')
        # 毎日
        if now_time_str == '19:59':
            await grablue_channel.send('@here 団アビ発動するポメ!')
        elif now_time_str == '21:59':
            await grablue_channel.send('2回目の団アビ発動し忘れてないポメ？')
        # 予選終了時
        if unite_and_fight_start_at + timedelta(days=2) == now:
            await grablue_channel.send('予選お疲れ様ポメ！明日はインターバルだポメ')
        # 本戦開始日
        if unite_and_fight_start_at + timedelta(days=3) == now:
            await grablue_channel.send('7:00から本戦だポメ、明日に備えて寝るポメ！')
        # 本戦時、毎日
        if unite_and_fight_start_at + timedelta(days=3) <= now:
            if now_time_str == '00:00':
                await grablue_channel.send('お疲れ様ポメ！')
            elif now_time_str == '07:00':
                await publicize_channel.send('今日の相手に勝ちに行くかと、現在の肉の個数をシートに記入するポメ!\n' + GSPREAD_URL + '\n14時時点で15人以上「勝ちに行く」なら勝ちにいく方針になるポメ\n忙しくて走れないと分かってる日は事前にその日を△にしとくといいポメ')
            elif now_time_str == '14:00':
                # TODO: シートのAPIで勝ちに行くの個数を取得してその結果によって発言を変えたい
                await publicize_channel.send(GSPREAD_URL + '\nアンケートの結果を見るポメ！15人以上「勝ちに行く」なら勝ちにいくポメ！')
    # 古戦場最終日
    elif unite_and_fight_end_at == now:
        await grablue_channel.send('本戦お疲れ様だポメ！明日はスペシャルバトルだポメ')

    # ドレバラ場期間中
    if (now - team_force_start_at).days == 0 and now_time_str == '19:00':
        await grablue_channel.send('ドレバラ開始だポメ！報酬全部取れるまで走るポメ！')
    elif (now - team_force_end_at).days == 0 and now_time_str == '19:00':
        await grablue_channel.send('ドレバラお疲れ様だポメ！')


async def lucifer(channel):
    """ ルシファーの募集をチャンネルに投げる
    """
    target_message = await channel.send('@here ダークラプチャー(HARD)の募集だポメ!\n要望がなければ21時開始だポメ\n参加する討伐方法でリアクションするポメ！\n\U0001F1E6: 通常\n\U0001F1E7: システム\n\U0001F1E8: どちらも可')
    reaction_list = [
        '\U0001F1E6', # A
        '\U0001F1E7', # B
        '\U0001F1E8', # C
    ]
    await add_reaction(target_message, reaction_list)


async def ultimate_bahamut(channel):
    """ アルバハHLの募集をチャンネルに投げる
    """
    target_message = await channel.send('@here アルバハHLの募集だポメ！\nリアクションした人から優先だポメ\n要望がなければ22時開始だポメ')
    await add_reaction(target_message, ['hai'])

async def proto_bahamut(channel):
    """ つよバハの募集をチャンネルに投げる
    """
    target_message = await channel.send('@here つよバハの募集だポメ！\n1部屋6人で自発者はサポでやるポメ\n要望がなければ21時開始だポメ')
    await add_reaction(target_message, ['hai'])

async def beelzebub(channel):
    """ バブさんの募集をチャンネルに投げる
    """
    target_message = await channel.send('@here バブさんの募集だポメ！\n要望がなければ21時開始だポメ\n参加する討伐方法でリアクションするポメ！\n\U0001F1E6: 通常\n\U0001F1E7: システム\n\U0001F1E8: どちらも可')
    reaction_list = [
        '\U0001F1E6', # A
        '\U0001F1E7', # B
        '\U0001F1E8', # C
    ]
    await add_reaction(target_message, reaction_list)

async def belial(channel):
    """ ベリアルの募集をチャンネルに投げる
    """
    target_message = await channel.send('@here ベリアルの募集だポメ！\n要望がなければ21時開始だポメ')
    await add_reaction(target_message, ['hai'])

async def add_reaction(message, reaction_list):
    """ スタンプをメッセージに追加する
    """
    emoji_list = CLIENT.emojis
    emoji_hash = {emoji.name: emoji for emoji in emoji_list}
    for reaction in reaction_list:
        if reaction in emoji_hash.keys():
            await message.add_reaction(str(emoji_hash[reaction]))
        else:
            await message.add_reaction(reaction)


CLIENT.run(DISCORD_TOKEN)
