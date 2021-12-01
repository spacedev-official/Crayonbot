import io
import asyncio
from PycordPaginator import Paginator
import discord
from discord import colour
from discord.ext import commands
import datetime

class util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name = "서버정보"
    )
    async def server_info(self, ctx):
        guild = self.bot.get_guild(ctx.guild.id)
        if ctx.guild.premium_subscription_count == 1:
            embed = discord.Embed(colour=0xff00, title=f"<:boosting0:732546134018621460> {ctx.guild.name}", timestamp=ctx.message.created_at)
        elif ctx.guild.premium_tier == 1:
            embed = discord.Embed(colour=0xff00, title=f"<:boosting1:732546134542909500> {ctx.guild.name}", timestamp=ctx.message.created_at)
        elif ctx.guild.premium_tier == 2:
            embed = discord.Embed(colour=0xff00, title=f"<:boosting2:732546134379331584> {ctx.guild.name}", timestamp=ctx.message.created_at)
        elif ctx.guild.premium_tier == 3:
            embed = discord.Embed(colour=0xff00, title=f"<:boosting3:732546133850587208> {ctx.guild.name}", timestamp=ctx.message.created_at)
        else:
            embed = discord.Embed(colour=0xff00, title=f"{ctx.guild.name}", timestamp=ctx.message.created_at)
        embed.add_field(name="서버 이름", value=ctx.guild.name, inline=False)
        embed.add_field(name="서버 ID", value=ctx.guild.id, inline=False)
        embed.add_field(name="서버 주인", value=f"{ctx.guild.owner}({ctx.guild.owner.mention})", inline=False)
        embed.add_field(name="서버 국가", value=ctx.guild.region, inline=False)
        embed.add_field(name="서버 제작일", value = ctx.guild.created_at.strftime("20%y년 %m월 %d일"), inline=False)
        embed.add_field(name="서버 멤버 수", value = f'전체 유저 : {len(ctx.guild.members)}명\n └ 유저 : {len([x for x in guild.members if not x.bot])}명 | 봇 : {len([x for x in ctx.guild.members if x.bot])}개', inline=False)
        embed.add_field(name="서버 채널 수", value = f'전체 채널 : {len(ctx.guild.channels)}개\n └ 채팅채널 : {len(ctx.guild.text_channels)}개 | 음성채널 : {len(ctx.guild.voice_channels)}개 | 카테고리 : {len(ctx.guild.categories)}개', inline=False)
        embed.add_field(name="서버 이모지 수", value = f'{len(ctx.guild.emojis)}개', inline=False)

        if ctx.guild.afk_channel != None:
            embed.add_field(name=f'서버 잠수 채널', value=f'⭕ | 잠수 채널이 존재합니다.({ctx.guild.afk_channel.name} (타이머: {ctx.guild.afk_timeout}))', inline=False)
        else:
            embed.add_field(name=f'서버 잠수 채널', value=f'❌ | 잠수 채널이 존재하지 않습니다.', inline=False)
        if ctx.guild.system_channel != None:
            embed.add_field(name=f'서버 시스템 채널', value=f'⭕ | 시스템 채널이 존재합니다.({ctx.guild.system_channel.name} (<#{ctx.guild.system_channel.id}>))', inline=False)
        else:
            embed.add_field(name=f'서버 시스템 채널', value=f'❌ | 시스템 채널이 존재하지 않습니다.', inline=False)
        embed.add_field(name=f'서버 부스트 레벨', value=f'Level {ctx.guild.premium_tier}', inline=False)
        embed.add_field(name=f'서버 부스트 개수', value=f'Boost {ctx.guild.premium_subscription_count}', inline=False)
        if ctx.guild.is_icon_animated() is True:
            a = ctx.guild.icon_url_as(format="gif", size=2048)
            embed.set_thumbnail(url=a)
        elif ctx.guild.is_icon_animated() is False:
            a = ctx.guild.icon_url_as(format="png", size=2048)
            embed.set_thumbnail(url=a)
        try:
            embed.set_image(url=ctx.guild.banner_url_as(format='png'))
        except:
            pass
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)



    @commands.command(name="프사")
    async def avatar(self, ctx, member: discord.Member = None):
        member_obj = member or ctx.author
        em = discord.Embed(
            title=f"{member}님의 프로필 사진",
            description=f"[링크]({member_obj.avatar_url})",
            colour=discord.Colour.random()
        )
        em.set_image(url=member_obj.avatar_url)
        await ctx.reply(embed=em)

    @commands.command(name="유저정보")
    async def userinfo(self, ctx, member: discord.Member = None):
        date = datetime.datetime.utcfromtimestamp(((int(ctx.author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(color=0xffff00, title=f'{member.name} 님의 정보') 
        embed.add_field(name="`이름`", value=member.name, inline=False) 
        embed.add_field(name="`별명`", value=member.display_name) 
        embed.add_field(name="`디스코드 가입일`", value=str(date.year) + "년 " + str(date.month) + "월 " + str(date.day) + "일", inline=False) 
        embed.add_field(name="`서버 가입일`", value=f"{(member.joined_at).year}년 {(member.joined_at).month}월 {(member.joined_at).day}일", inline=False) 
        embed.add_field(name="`아이디`", value=member.id) 
        embed.add_field(name="`최상위 역할`", value=member.top_role.mention, inline=False) 
        embed.set_thumbnail(url=member.avatar_url) 
        await ctx.send(embed=embed) 

    @commands.command(
    name = "내정보"
    )
    async def my_info(self, ctx):
        date = datetime.datetime.utcfromtimestamp(((int(ctx.author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(color=0xffff00, title=f'{ctx.author.name} 님의 정보') 
        embed.add_field(name="`이름`", value=ctx.author.name, inline=False) 
        embed.add_field(name="`별명`", value=ctx.author.display_name) 
        embed.add_field(name="`디스코드 가입일`", value=str(date.year) + "년 " + str(date.month) + "월 " + str(date.day) + "일", inline=False) 
        embed.add_field(name="`서버 가입일`", value=f"{(ctx.author.joined_at).year}년 {(ctx.author.joined_at).month}월 {(ctx.author.joined_at).day}일", inline=False) 
        embed.add_field(name="`아이디`", value=ctx.author.id) 
        embed.add_field(name="`최상위 역할`", value=ctx.author.top_role.mention, inline=False) 
        embed.set_thumbnail(url=ctx.author.avatar_url) 
        await ctx.send(embed=embed) 
def setup(bot):
    bot.add_cog(util(bot))