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
import datetime

ticket_guild_id = 856829534926143538
category_id = 890151936819617822
close_ticket_category_id = 895287042882281532

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