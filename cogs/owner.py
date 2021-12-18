import discord
from discord.embeds import Embed
from discord.ext import commands, tasks
import asyncio
import random
import os
from discord.ext.menus import Button
from discord_components import component
from discord_components import Button, ButtonStyle, SelectOption, Select
import pytz
import aiosqlite
import discordSuperUtils
import datetime
from PycordPaginator import Paginator

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "서버리스트",
        aliases = ['serverlist']
    )
    @commands.is_owner()
    async def owner_serverlist(self, ctx):
        with open("guilds.txt", 'w', -1, "utf-8") as a: # 'guilds.txt' 파일을 생성하고 그것을 'a' 로 지정한다
            a.write(str(self.bot.guilds)) # 'a' 에 봇이 접속한 서버들을 나열한다 
        file1 = discord.File("guilds.txt") # 'file1' 을 'guilds.txt' 로 정의한다
        await ctx.author.send(file=file1) # 명령어를 수행한 멤버의 DM으로 'file1' 을 발송한다
        os.remove("guilds.txt")
        await ctx.reply(f"DM으로 서버 리스트 발송을 완료했습니다!")

    @commands.command(
        name="Check-Error",
        aliases=["elog"],
        usage="elog [code]",
        help=" 코인의 에러 로그를 확인할수 있습니다.",
        hidden=True,
    )
    @commands.is_owner()
    async def owner_elog(self, ctx, code):
        try:
            f = open(f"data/error_logs/{code}", "r", encoding="utf8")
            data = f.read()
            await ctx.send(f"```py\n{data}\n```")
            f.close()
        except:
            await ctx.send(
                content=code, file=discord.File(fp=data, filename=f"{code}.txt")
            )

    @commands.command(name="공지")
    @commands.is_owner()
    async def broadcasting(self, ctx, *, value):
        em = discord.Embed(
            title="짱구 봇 공지사항",
            description=value,
            colour=discord.Colour.random()
        )
        em.set_thumbnail(url=self.bot.user.avatar_url)
        em.set_image(
            url="https://media.discordapp.net/attachments/921555509935480853/921555519578189834/c265877614d80026.png?width=400&height=144")
        em.set_footer(text="특정 채널에 받고싶다면 '짱구야 설정'으로 설정하세요! 권한 확인 필수!")
        msg = await ctx.reply("발송중...")
        guilds = self.bot.guilds
        ok = []
        ok_guild = []
        success = 0
        failed = 0
        for guild in guilds:
            channels = guild.text_channels
            for channel in channels:
                if guild.id in [653083797763522580, 786470326732587008]:
                    break
                if (
                    channel.topic is not None
                    and str(channel.topic).find("-HOnNt") != -1
                ):
                    ok.append(channel.id)
                    ok_guild.append(guild.id)
                    break

        for guild in guilds:
            channels = guild.text_channels
            for _channel in channels:
                if guild.id in ok_guild:
                    break
                if guild.id in [653083797763522580, 786470326732587008]:
                    break
                random_channel = random.choices(channels)
                ok.append(random_channel[0].id)
                break
        for i in ok:
            channel = self.bot.get_channel(i)
            try:
                await channel.send(embed=em)
                success += 1
            except discord.Forbidden:
                failed += 1
        await msg.edit("발송완료!\n성공: `{ok}`\n실패: `{no}`".format(ok=success, no=failed))
    @commands.group(name="블랙",invoke_without_command=True)
    async def blacklist(self,ctx:commands.Context):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM black WHERE user = ?", (ctx.author.id,))
        if await cur.fetchone() == None:
            return await ctx.reply(f"{ctx.author}님은 블랙리스트에 등록되어있지 않아요.")
        data = await cur.fetchone()
        await ctx.reply(f"블랙사유: {data[1]}")
    @blacklist.command(name= '추가', aliases=['black','블랙','blackadd'])
    @commands.is_owner()
    async def mod_black(self, ctx, user_id:int,*,reason):
        user = await self.bot.fetch_user(user_id)
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM black WHERE user = ?", (user_id,))
        datas = await cur.fetchone()
        if datas != None:
            embed = discord.Embed(
                title = f"블랙",
                description = f"{user}님은 블랙리스트에 등록되어있어요. \n사유: {datas[1]}",
                colour = discord.Colour.random(),
                timestamp = ctx.message.created_at
            )
            await ctx.send(embed=embed)
        await db.execute("INSERT INTO black(user,reason,username) VALUES (?,?,?)", (user_id, reason, user.name))
        await db.commit()
        embed2=discord.Embed(
            title="블랙",
            description = f"__봇관리자로 부터 블랙 등록되었음을 알려드립니다__ \n\n 관리자가 아래의 사유로 블랙을 등록하셨어요.\n\n 사유 : {reason}",
            colour=discord.Colour.random() )
       
        try:
            await user.send(embed=embed2)
        except:
            pass
        await ctx.reply("등록완료!")
    @blacklist.command(name= '삭제', aliases=['blackdel','제거'])
    @commands.is_owner()
    async def mod_black_del(self, ctx, user_id:int):
        user = await self.bot.fetch_user(user_id)
        db = await aiosqlite.connect("db/db.sqlite")
        cur = await db.execute("SELECT * FROM black WHERE user = ?", (user_id,))
        datas = await cur.fetchone()
        embed=discord.Embed(title="블랙", description=f"{user}님은 블랙리스트에 등록되어있지않아요.",colour=discord.Colour.random())
        if datas ==  None:
            return await ctx.send(embed=embed)
        await db.execute("DELETE FROM black WHERE user = ?", (user_id,))
        await db.commit()
        embed2=discord.Embed(title="블랙", description="__봇 관리자로부터 블랙해제됨.__\n\n 봇관리자가 블랙해제하셨어요.",colour=discord.Colour.random())
        try:
            await user.send(embed=embed2)
        except:
            print
        await ctx.reply("해제완료")
    @blacklist.command(name= '목록')
    @commands.is_owner()
    async def mod_black_jo(self, ctx):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM black")
        datas = await cur.fetchall()
        black_list = []
        for i in datas:
            black_list.append(f"```유저아이디|{i[0]} \n사유|{i[1]} \n이름|{i[2]}```")       
        e = Paginator(
                client=self.bot.components_manager,
                embeds=discordSuperUtils.generate_embeds(
                    black_list,
                    title=f"블랙목록에 유저들이 등록되어있어요.",
                    fields=10,
                    description="```블랙해제를 하실거면 \n짱구야 블랙 제거 [유저아이디]를 해주시면 됩니다!```",
                ),
                channel=ctx.channel,
                only=ctx.author,
                ctx=ctx,
                use_select=False)
        await e.start()
            #await ctx.send(templates[1])
    @blacklist.command(name= '초기화', aliases=["reset"])
    @commands.is_owner()
    async def black_rest(self, ctx):
        db = await aiosqlite.connect("db/db.sqlite")
        await db.execute("DELETE FROM black")
        await db.commit()
        
        cur = await db.execute("SELECT * FROM black")
        datas = await cur.fetchall()
        if datas != None:
            await ctx.reply("초기화 완료")

    
        # for i in self.bot.guilds:
        #     for j in i.text_channels:
        #         if ("코인" in j.topic):
        #             try:
        #                 await j.send(embed=embed)
        #                 count += 1
        #                 channel.append(f"{i.name} - {j.name}")
        #             except:
        #                 for k in i.text_channels:
        #                     if ("봇" in k.name):
        #                         try:
        #                             await k.send(embed=embed)
        #                             count += 1
        #                             channel.append(f"{i.name} - {j.name}")
        #                         except:
        #                             for l in i.text_channels:
        #                                 if ("공지" in l.name):
        #                                     try:
        #                                         await i.send(embed = embed)
        #                                         count += 1
        #                                         channel.append(f"{i.name} - {l.name}")
        #                                     except:
        #                                         channel.append(f"{i.name} 전송 실패")
        #                                     break                                            
        #             else:
        #                 break
        # await ctx.send(f"{count}개의 길드에 공지를 전송했습니다!")

def setup(bot):
    bot.add_cog(Owner(bot))