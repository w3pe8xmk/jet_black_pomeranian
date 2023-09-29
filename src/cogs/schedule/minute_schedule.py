from datetime import datetime, timedelta, timezone

from discord.ext import commands, tasks


class MinuteSchedule(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.JST = timezone(timedelta(hours=+9), 'JST')

    async def cog_load(self):
        self.loop.start()

    async def cog_unload(self):
        self.loop.cancel()

    @tasks.loop(seconds=60)
    async def loop(self):
        """ 定期発言(60秒に一回ループ)
        """

        now = datetime.now(self.JST).replace(second=0, microsecond=0)
        now_time_str = now.strftime('%H:%M')

        # 古戦場のスケジュール
        unite_and_fight_schedule = self.bot.schedule['unite_and_fight']
        max_unite_and_fight_schedule = max(unite_and_fight_schedule.items())[1]
        unite_and_fight_start_at = datetime.strptime(
            max_unite_and_fight_schedule['start_at'],
            '%Y/%m/%d %z'
        )
        unite_and_fight_end_at = datetime.strptime(
            max_unite_and_fight_schedule['end_at'],
            '%Y/%m/%d %z'
        )
        # ドレバラのスケジュール
        team_force_schedule = self.bot.schedule['team_force']
        max_team_force_schedule = max(team_force_schedule.items())[1]
        team_force_start_at = datetime.strptime(
            max_team_force_schedule['start_at'],
            '%Y/%m/%d %z'
        )
        team_force_end_at = datetime.strptime(
            max_team_force_schedule['end_at'],
            '%Y/%m/%d %z'
        )

        # 古戦場3日前
        if unite_and_fight_start_at - timedelta(days=3) == now:
            await self.bot.grablue_channel.send('3日後に古戦場が始まるポメ\n各自個人のアサルトタイムを見直すポメ！')
        # 古戦場1日前
        if unite_and_fight_start_at - timedelta(days=1) == now:
            await self.bot.grablue_channel.send(
                '明日から古戦場だポメ、次回古戦場シートに一言と目標を記入するポメ！\n'
                + self.bot.GSPREAD_URL
            )
        # 古戦場期間中
        if unite_and_fight_start_at < now < unite_and_fight_end_at:
            # 予選開始時
            if unite_and_fight_start_at + timedelta(hours=19) == now:
                await self.bot.grablue_channel.send('古戦場予選開始ポメ。応援してるポメ！')
            # 毎日
            if now_time_str == '19:59':
                await self.bot.grablue_channel.send('@here 団アビ発動するポメ!')
            elif now_time_str == '21:59':
                await self.bot.grablue_channel.send('2回目の団アビ発動し忘れてないポメ？')
            # 予選終了時
            if unite_and_fight_start_at + timedelta(days=2) == now:
                await self.bot.grablue_channel.send('予選お疲れ様ポメ！明日はインターバルだポメ')
            # 本戦開始日
            if unite_and_fight_start_at + timedelta(days=3) == now:
                await self.bot.grablue_channel.send('7:00から本戦だポメ、明日に備えて寝るポメ！')
            # 本戦時、毎日
            if unite_and_fight_start_at + timedelta(days=3) <= now:
                if now_time_str == '00:00':
                    await self.bot.grablue_channel.send('お疲れ様ポメ！')
                elif now_time_str == '07:00':
                    await self.bot.publicize_channel.send(
                        '今日の相手に勝ちに行くかをシートに記入するポメ!\n'
                        + self.bot.GSPREAD_URL
                        + '\n14時時点で15人以上「勝ちに行く」なら勝ちにいく方針になるポメ\n'
                        + '忙しくて走れないと分かってる日は事前にその日を△にしとくといいポメ'
                    )
                elif now_time_str == '14:00':
                    # TODO: シートのAPIで勝ちに行くの個数を取得してその結果によって発言を変えたい
                    await self.bot.publicize_channel.send(
                        self.bot.GSPREAD_URL
                        + '\nアンケートの結果を見るポメ！15人以上「勝ちに行く」なら勝ちにいくポメ！')
        # 古戦場最終日
        elif unite_and_fight_end_at == now:
            await self.bot.grablue_channel.send('本戦お疲れ様だポメ！明日はスペシャルバトルだポメ')

        # ドレバラ場期間中
        if (now - team_force_start_at).days == 0 and now_time_str == '19:00':
            await self.bot.grablue_channel.send('ドレバラ開始だポメ！報酬全部取れるまで走るポメ！')
        elif (now - team_force_end_at).days == 0 and now_time_str == '19:00':
            await self.bot.grablue_channel.send('ドレバラお疲れ様だポメ！')


async def setup(bot: commands.Bot):
    await bot.add_cog(MinuteSchedule(bot))
