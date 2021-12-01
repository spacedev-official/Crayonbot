import datetime
import time

import aiosqlite
import discord
import discordSuperUtils
from discord.ext import commands
from pycord_components import (
    Select,
    SelectOption,
    Interaction,
    Button
)


class InviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()
        self.InviteTracker = discordSuperUtils.InviteTracker(self.bot)


    @commands.group(name="출석체크", aliases=["출쳌", "출첵"], invoke_without_command=True)
    async def chulcheck(self, ctx):
        now = datetime.datetime.now()
        dates = f"{now.year}-{now.month}-{now.day}"
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM chulcheck WHERE user = ? AND stand = ?", (ctx.author.id, dates))
        res = await cur.fetchone()
        if res is not None:
            times = res[1]
            timestamp = time.mktime(datetime.datetime.strptime(times, '%Y-%m-%d %H:%M:%S').timetuple())
            return await ctx.reply(f"이미 출석체크를 하셨어요!\n출석체크일시 - <t:{str(timestamp)[:-2]}:R>")
        await db.execute("INSERT INTO chulcheck(user) VALUES (?)", (ctx.author.id,))
        await db.commit()
        dates = f"{now.year}-{now.month}-{now.day}"
        await ctx.reply(f"출석체크를 완료했어요!\n출석체크일시 - {now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}")
        cur = await db.execute("SELECT * FROM chulcheck WHERE stand = ? ORDER BY dates", (dates,))
        res = await cur.fetchall()
        check_list = [
            f"{num}. {self.bot.get_user(i[0])} | {i[1]}"
            for num, i in enumerate(res, start=1)
        ]

        leaderboard = "\n".join(check_list)
        em = discord.Embed(
            title="오늘의 출석체크 리더보드",
            description=f"누가 가장먼저 출석체크를 했을까요?```fix\n{leaderboard}```"
        )
        await ctx.send(embed=em)

    @chulcheck.command(name="리더보드")
    async def chulcheck_leaderboard(self,ctx):
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM chulcheck")
        res = await cur.fetchall()
        dates = [i[2] for i in res]
        new_dates = []
        for i in dates:
            if i not in new_dates:
                new_dates.append(i)
        async def btn_callback(interaction: Interaction):
            if interaction.custom_id == "close":
                await interaction.message.delete()
        async def callback(interaction: Interaction):
            values = interaction.values[0]
            if interaction.user.id == ctx.author.id:
                cur = await db.execute("SELECT * FROM chulcheck WHERE stand = ? ORDER BY dates", (values,))
                res = await cur.fetchall()
                check_list = []
                num = 0
                for i in res:
                    num += 1
                    check_list.append(f"{num}. {self.bot.get_user(i[0])} | {i[1]}")
                leaderboard = "\n".join(check_list)
                # cur = await db.execute("SELECT * FROM chulcheck", (dates,))
                # res = await cur.fetchall()
                em = discord.Embed(
                    title=f"{values} | 출석체크 리더보드",
                    description=f"누가 가장먼저 출석체크를 했을까요?```fix\n{leaderboard}```"
                )
                """dates_two = [i[2] for i in res]
                new_dates_two = []
                for i in dates_two:
                    if i not in new_dates_two:
                        new_dates_two.append(i)"""
                await interaction.edit_origin(embed=em,
                                              components=[
                                                  self.bot.components_manager.add_callback(
                                                      Select(
                                                          options=[
                                                              SelectOption(label=i, value=i) for i in new_dates
                                                          ],
                                                      ),
                                                      callback,
                                                  ),
                                                  self.bot.components_manager.add_callback(
                                                      Button(label="메세지 닫기", style=4, custom_id="close", emoji="❎"
                                                             ),
                                                      btn_callback,
                                                  )
                                              ])


        print(new_dates)
        await ctx.reply(
            "조회할 리더보드 일정을 선택해주세요.",
            components=[
                self.bot.components_manager.add_callback(
                    Select(
                        options=[
                            SelectOption(label=i, value=i) for i in new_dates
                        ],
                    ),
                    callback,
                ),
                self.bot.components_manager.add_callback(
                    Button(label="메세지 닫기",style=4,custom_id="close",emoji="❎"
                    ),
                    btn_callback,
                )
            ]
        )


def setup(bot):
    bot.add_cog(InviteTracker(bot))
