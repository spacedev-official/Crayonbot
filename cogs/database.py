import imp
from re import T
from click import command
import discord
from discord import colour
from discord.ext import commands
import time
import random
import sqlite3
import requests
import traceback
import asyncio

import discordSuperUtils
import os
import psutil
import random
import asyncio
import datetime
import time
import aiosqlite
from PycordPaginator import Paginator
con = sqlite3.connect(f'db/db.sqlite')
cur = con.cursor()

admin = [0]
black = [0]
vip = [0]
users = [0]

class Database(commands.Cog, name = "봇 경제 명령어", description = "봇 경제 명령어"):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name = f'가입')
    async def data_join(self, ctx):
        try:

            # await ctx.send(f'{ctx.author.mention}, [약관](https://blog.teamsb.cf/pages/tos)을 동의하시려면 이 채널에 `동의` 를 입력해 주세요.\n동의하지 않으신다면 그냥 무시하세요.')
            embed = discord.Embed(
                title = '가입',
                description = '이용 약관을 동의하시려면 이 채널에 `동의` 를 입력해 주세요.\n이용 약관을 동의하지 않으신다면 이 메시지를 무시하세요.',
                colour = discord.Colour.green()
            )
            await ctx.send(f'{ctx.author.mention}', embed = embed)

            def check(m):
                return m.content == '동의' and m.author.id == ctx.author.id

            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f"<a:no:754265096813019167> {ctx.author.mention}, 시간이 초과되어 자동 종료되었습니다.")
            else:
                if msg.content == "동의":
                    try:
                        cur.execute(f'INSERT INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (str(ctx.author.id), str(ctx.author.name), 0, 0, 0, 0, 0, 0, random.randint(1, 4), 0, "None"))
                        con.commit()
                    except sqlite3.IntegrityError:
                        await ctx.send(f'{ctx.author.mention}님은 이미 가입된 유저입니다.')
                        con.commit()
                        return None
                    except sqlite3.OperationalError:
                        await ctx.send(f'{ctx.author.mention}님 가입 진행중 데이터베이스에 문제가 생겼습니다. \n계속해서 같은 오류가 뜬다면 Bainble0211#6109에게 문의해 주세요!\n에러 : ```python\n{traceback.format_exc()}\n```')
                        con.commit()
                        return None
                    await ctx.send(f'{ctx.author.mention}님의 가입을 성공하였습니다!')
                        # else:
                        #     await ctx.send(f'{ctx.author.mention} 다른 것을 입력하셨거나, 무시하셔서 취소되었습니다.')
                        #     return None
        except:
            await ctx.send(traceback.format_exc())

    @commands.command(name = f'구입')
    async def data_buy(self, ctx, *, args):
        if args == '' or args == ' ':
            await ctx.send(f'구입할 물건의 이름을 입력해 주세요!')
            return None
        i = 0
        cur.execute(f'SELECT * FROM USERS WHERE ID=\'{ctx.author.id}\'')
        for row in cur:
            user = row
            i += 1
        if i == 0:
            await ctx.send(f'{ctx.author.mention}님은 코인봇 데이터베이스에 존재하지 않는 유저입니다. 가입을 해주세요!')
            return None
        if args in ['이름변경', '닉변권', '닉변티켓', '이름변경티켓']:
            if user[2] < 5000:
                await ctx.send(f'{ctx.author.mention}님이 보유하신 금액이 부족합니다.')
                return None
            cur.execute(f'UPDATE USERS SET money={user[2] - 5000}, customcommands={user[3] + 10} WHERE id=\'{user[0]}\'')
            con.commit()
            await ctx.send(f'{ctx.author.mention}님 닉변 티켓을 구매완료했습니다!\n닉변 티켓 사용은 `관리자` 에게 `닉변할 이름을` 적어 주시면 24시간 내에 생성됩니다!')
            return None
        if args in ['vip', 'VIP']:
            if user[2] < 100000:
                await ctx.send(f'{ctx.author.mention}님이 보유하신 금액이 부족합니다.')
                return None
            if user[4] != 0:
                await ctx.send(f'{ctx.author.mention}님은 이미 VIP입니다.')
                return None
            cur.execute(f'UPDATE USERS SET money={user[2] - 1000000}, vip={1} WHERE id=\'{user[0]}\'')
            con.commit()
            await ctx.send(f'{ctx.author.mention}님의 VIP권 구매를 완료했습니다!')
            return None
        else:
            await ctx.send(f'{args}은/는 아직 상점에 등록되지 않은 물건입니다.')
            return None

    @commands.command(name = f'인벤', aliases = ['인벤토리', '가방', '내가방'])
    async def data_inventory(self, ctx):
        i = 0
        cur.execute(f'SELECT * FROM USERS WHERE id=\'{ctx.author.id}\'')
        for row in cur:
            i += 1
            user2 = row
        if i == 0:
            await ctx.send(f'{ctx.author.mention}님은 짱구의 데이터베이스에 등록되어 있지 않습니다.')
            return None
        embed=discord.Embed(title=f"{ctx.author.name}님의 인벤토리", colour=discord.Colour.random())
        embed.add_field(name="보유한 돈", value=f"{user2[2]}")
        embed.add_field(name="닉변권", value=f"{user2[3]}")
        embed.add_field(name="VIP권", value=f"{user2[4]}")
        await ctx.send(embed=embed)
    @commands.command(name = f'유저인벤', aliases = ['유저인벤토리', '유저가방'])
    async def member_inventory(self, ctx, member:discord.Member):
        i = 0
        res=cur.execute(f'SELECT * FROM USERS WHERE id=\'{member.id}\'')
        if res ==  None:
            return await ctx.reply("가입되지 않은 유저입니다.")
        for row in cur:
            i += 1
            user2 = row
        if i == 0:
            await ctx.send(f'{ctx.author.mention}님은 짱구의 데이터베이스에 등록되어 있지 않습니다.')
            return None
        embed=discord.Embed(title=f"{member.name}님의 인벤토리", colour=discord.Colour.random())
        embed.add_field(name="보유한 돈", value=f"{user2[2]}")
        embed.add_field(name="닉변권", value=f"{user2[3]}")
        embed.add_field(name="VIP권", value=f"{user2[4]}")
        await ctx.send(embed=embed)
    @commands.command(
        name= "송금",
    )
    async def songgm(self, ctx, member: discord.Member, money: int):
        try:
            database = await aiosqlite.connect("db/db.sqlite")
            cur1=await database.execute(f"SELECT * FROM USERS WHERE id=\'{ctx.author.id}\'")
            cur2=await database.execute(f"SELECT * FROM USERS WHERE id=\'{member.id}\'")
            datas = await cur1.fetchall()
            datas1 = await cur2.fetchall()
            embed=discord.Embed(title="송금완료", description = f"송금된 돈: {money}", colour=discord.Colour.random())
            for user in datas:
                # await database.execute(f"UPDATE USERS SET money={user[2] + money} WHERE id=\'{member.id}\'")
                # await asyncio.sleep(2)
                await database.execute(f"UPDATE USERS SET money={user[2] - money} WHERE id=\'{ctx.author.id}\'")
                await database.commit()
                embed.add_field(name=f"보낸 사람: {ctx.author.name}", value=f" 현재 돈: {user[2]}")
            for user in datas1:
                await database.execute(f"UPDATE USERS SET money={user[2] + money} WHERE id=\'{member.id}\'")
                await database.commit()
                embed.add_field(name=f"받은 사람: {member.name}" , value=f" 현재돈: {user[2]}")
            
            await ctx.reply(embed=embed)
        except:
            print(traceback.format_exc())
    @commands.command(name = f'지원금', aliases = ['ㅈㅇㄱ'])
    async def data_givemoney(self, ctx):
        try:
            i = 0
            cur.execute(f'SELECT * FROM USERS WHERE id=\'{ctx.author.id}\'')
            for row in cur:
                user = row
                i += 1
            if i == 0:
                await ctx.send(f'{ctx.author.mention}님은 짱구봇 서비스에 가입되어 있지 않습니다.')
                return None
            if not int(user[9] + 3600 - time.time()) <= 0:
                await ctx.send(f'{int(user[9] + 3600 - time.time())}초 동안 쿨타임이 적용되어있습니다')
                return None
            randmoney = random.randint(1, 1000)
            cur.execute(f'UPDATE USERS SET money={user[2] + randmoney}, cooltime={time.time()} WHERE id=\'{user[0]}\'')
            con.commit()
            await ctx.send(f'{ctx.author.mention}님에게 {randmoney}원이 적립되었습니다!')
        except:
            print(traceback.format_exc())
    @commands.command(name = '도박', aliases = ["ㄷㅂ"])
    async def data_gambling(self, ctx, money):
        try:
            date = cur.execute("SELECT * FROM USERS WHERE ID = ?", (str(ctx.author.id),)).fetchone()
            if not date:
                await ctx.send(f'{ctx.author.mention}님! 도박을 하기 전에 짱구봇 서비스에 가입해 주세요!\n가입 명령어 : `짱구야 가입`')
                return None


            if int(money) > date[2]:
                await ctx.send('가진돈 보다 더 많은 돈으로는 도박할수 없어요!')
                return None
            if int(money) == 0:
                await ctx.send(f'0 보다 적은돈으로는 도박을 할수 없어요!')
                return None

            
            cur.execute(f'SELECT * FROM USERS WHERE id=\'{ctx.author.id}\'')
            for row in cur:
                user2 = row
            original_money = user2[2]
            
            embed = discord.Embed(
                    title = f'{money}원을 가지고 도박 하셨습니다!',
                    colour = discord.Colour.green()
                )
            await ctx.send(embed=embed)

            random_value = random.randint(1, 3)
            on = 0
            getmoney = 0
            if random_value == 1 or random_value == 3:
                on = 1
                getmoney = int(money + money)
            else:
                on = 2
                getmoney = int(money) * -1
                lostmoney = int(money)

                                #await ctx.send(f"{data}") # 유일하게 여기만 user에 노란줄이 없음 왜이럴까
            print(original_money)
            print(getmoney, date[0])
            print(type(original_money))
            # print(type(getmoney, date[0])) # 얘는 안나오잖아 아 뭔지 알았어
            print((int(original_money) + int(getmoney)))
            print(type(int(original_money) + int(getmoney)))
                # ? 잠만 왜 저게 getmoney, date 두개가 한개 안에 들어가있어
            try:
                cur.execute("UPDATE USERS SET money = ? WHERE id = ?",(int(original_money) + int(getmoney),ctx.author.id)) # ㅌㅌ ?
            except:
                print(traceback.format_exc())
                #cur.execute("UPDATE USERS SET username = ? WHERE id = ?",(getmoney,date[0])) # 하셈
                    #cur.execute(f'UPDATE USERS SET MONEY = {user[2] + getmoney} WHERE id =\'{user[0]}\'') # 위에서는 user에서 노란줄이 뜨는데 여기만 안떠
                    # 실행해봐
            con.commit()

            if on == 1:
                await ctx.send(f'{ctx.author.mention} 도박을 성공했어요! {getmoney} 원을 적립했어요!')
                return None
            if on == 2:
                await ctx.send(f'{ctx.author.mention} 도박을 실패했어요.... {lostmoney}원을 짱구가 가져갈게요~! 감사합니당!')
                return None
        except:
            await ctx.send(traceback.format_exc())
    @commands.command(name = '유저목록', aliases = ["도박목록"])
    @commands.has_permissions(administrator=True)
    async def ecoinfo(self, ctx):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM USERS")
        datas = await cur.fetchall()
        now = datetime.datetime.now()
        black_list = []
        for i in datas:
            black_list.append(f"```유저아이디|{i[0]} \n이름|{i[1]} \n돈|{i[2]} \n닉변권|{i[3]} \nvip|{i[4]}```")
        e = Paginator(
                client=self.bot.components_manager,
                embeds=discordSuperUtils.generate_embeds(
                    black_list,
                    title=f"도박을 사용하는 유저들이 등록되어있어요.",
                    fields=10,
                    description=f"```현재 시간 \n {now.year}년 {now.month}월 {now.day}일 {now.hour:02}시 {now.minute:02}분 ```",
                ),
                channel=ctx.channel,
                only=ctx.author,
                ctx=ctx,
                use_select=False)
        await e.start()
    @commands.command(name="목록")
    async def ecolist(self, ctx):
        embed=discord.Embed(title="구입목록", colour=discord.Colour.random())
        embed.add_field(name="목록", value="```1, 닉변권```")
        await ctx.reply(embed=embed)
def setup(bot):
    bot.add_cog(Database(bot))
