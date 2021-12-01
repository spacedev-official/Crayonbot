from os import name
import discord
from discord import message
from discord import embeds
from discord import mentions
from discord.ext import commands

from discord_components import Button, ButtonStyle, SelectOption, Select, component
import discord_components


import os
import psutil
import random
import asyncio
import datetime
import time

from utils.json import loadjson, savejson


from discord.ext.commands.core import Command, command

class management(commands.Cog, name = "서버 관리 명령어", description = "서버 관리 명령어 Cog입니다."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name= '킥', aliases=['추방','kick'])
    @commands.has_permissions(administrator=True)
    async def mod_kick(self, ctx, member: discord.Member, *, reason: str = None):
        embed = discord.Embed(
            title = f"추방",
            description = f"유저를 킥했습니다.\n\n대상: {member}\n관리자: {ctx.author}\n사유: {reason}",
            colour = discord.Colour.dark_orange(),
            timestamp = ctx.message.created_at
        )
        await ctx.send(embed=embed)
        await member.send(embed = embed)
        await ctx.guild.kick(member, reason = reason)
    
    @commands.command(name= '밴', aliases=['차단','ban'])
    @commands.has_permissions(administrator=True)
    async def mod_ban(self, ctx, member: discord.Member, *, reason: str = None):
        embed = discord.Embed(
            title = "밴",
            description = f"유저를 밴했습니다.\n\n대상: {member}\n관리자: {ctx.author}\n사유: {reason}",
            colour = discord.Colour.red(),
            timestamp = ctx.message.created_at
            
        )
        await ctx.send(embed = embed)
        await member.send(embed = embed)
        await ctx.guild.ban(member, reason = reason)
    @commands.command(name="언밴")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, user: discord.User):
        await self.BanManager.connect_to_database(self.bot.db, ["bans"])
        if await self.BanManager.unban(user, guild=ctx.guild):
            await ctx.send(f"{user}님은 언밴되셨어요.")
        else:
            await ctx.send(f"{user}은 밴되어있지않아요.")
            
    @commands.command(name= '뮤트', aliases = ["mute"])
    @commands.has_permissions(administrator=True)
    async def mod_mute(self, ctx,  user: discord.User, *,reason: str = None):
        msg = await ctx.send(
            embed= discord.Embed(title= "뮤트",description=f"{user} 유저에게 {reason}의 사유로 뮤트를 하시겠습니까?"),
            components = [
                [
                    Button(label="네", emoji="✅", style=ButtonStyle.green, id="yes"),
                    Button(label="아니요", emoji="❎", style=ButtonStyle.red, id="no"),
                ]
            ]
        )
        def check(res):
            return ctx.author == res.user and res.channel == ctx.channel

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=60)
            if res.component.id == "no":
                return await msg.edit(content = "취소하였습니다.", components = [])
        except asyncio.TimeoutError:
            return await msg.edit(content = "시간 초과로 취소되었습니다.", components = [])
        role = discord.utils.get(ctx.guild.roles, name = "🚫 뮤트 🚫")
        await ctx.guild.get_member(user.id).add_roles(role)
        embed= discord.Embed(title="뮤트",description=f"뮤트를 완료했습니다")
        await msg.edit(embed=embed)
    @commands.command(name= '언뮤트', aliases = ["unmute"])
    @commands.has_permissions(administrator=True)
    async def mod_unmute(self, ctx,  user: discord.User, *,reason: str = None):
        msg = await ctx.send(
            embed= discord.Embed(title= "언뮤트",description=f"{user} 유저에게 {reason}의 사유로 언뮤트를 하시겠습니까?"),
            components = [
                [
                    Button(label="네", emoji="✅", style=ButtonStyle.green, id="yes"),
                    Button(label="아니요", emoji="❎", style=ButtonStyle.red, id="no"),
                ]
            ]
        )
        def check(res):
            return ctx.author == res.user and res.channel == ctx.channel

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=60)
            if res.component.id == "no":
                return await msg.edit(content = "취소하였습니다.", components = [])
        except asyncio.TimeoutError:
            return await msg.edit(content = "시간 초과로 취소되었습니다.", components = [])
        role = discord.utils.get(ctx.guild.roles, name = "🚫 뮤트 🚫")
        await ctx.guild.get_member(user.id).remove_roles(role)
        embed= discord.Embed(title="뮤트",description=f"언뮤트를 완료했습니다")
        await msg.edit(embed=embed)
    @commands.command(name="서버공지")
    @commands.has_permissions(administrator=True)
    async def notice_server(self, ctx, channel: discord.TextChannel, *, value):
        em = discord.Embed(
            title=f"{ctx.guild}공지사항",
            description=value,
            colour=discord.Colour.random()
        )

        await channel.send(embed=em)

    @commands.command(name = "청소", aliases = ["ㅊ"])
    @commands.has_permissions(administrator = True)
    async def clean(self, ctx, limit: int = None):
        if not type(limit) == int:
            return await ctx.reply("삭제할 수의 숫자 형식이어야 합니다.")
        await ctx.channel.purge(limit = limit + 1)
        await ctx.send(f"{limit}개의 메시지를 삭제하였습니다.", delete_after = 5)
            # role = discord.utils.get(ctx.guild.roles, name = "USER")
            # await user.add_roles(role)
            # await msg.edit(embed2=discord.Embed(title="인증", description="인증완료"))
    # msg = await ctx.send(embed = discord.Embed(title = "서버 스탯 채널 타입", description = "어떤 채널로 서버 스탯 채널을 생성하시겠습니까"), components = [
    #         [
    #             Button(label = "텍스트채널", emoji = "💬", style = ButtonStyle.gray, id = "textchannel"),
    #             Button(label = "스테이지 채널", emoji = "🎤", style = ButtonStyle.gray, id = "stagechannel"),
    #             Button(label = "음성 채널", emoji = "🔊", style = ButtonStyle.gray, id = "voicechannel"),
    #             Button(label = "취소", emoji = "❌", style = ButtonStyle.red, id = "cancel"),
    #         ]
    #     ])

        # def check(res):
        #     return res.user == ctx.author and res.channel == ctx.channel
        
        # try:
        #     res = await self.bot.wait_for("button_click", check = check, timeout = 60)
        #     if res.component.id == "cancel":
        #         return await ctx.send(embed = discord.Embed(title = "서버 스탯 채널 생성 취소", description = "서버 스탯 채널 생성을 취소하였습니다."))
        # except asyncio.TimeoutError:
        #     return await ctx.send(embed = discord.Embed(title = "서버 스탯 채널 생성 취소", description = "서버 스탯 채널 생성을 취소하였습니다."))
        
        # category = await ctx.guild.create_category_channel(name = "📊 서버 스탯")

        # if res.component.id == "textchannel":
        #     allChannel = await category.create_text_channel(name = f"총 멤버ㅣ {len(ctx.guild.members)}", position = 0)
        #     userChannel = await category.create_text_channel(name = f"유저 수ㅣ {len([x for x in ctx.guild.members if not x.bot])}", position = 1)
        #     botChannel = await category.create_text_channel(name = f"봇 수ㅣ {len([x for x in ctx.guild.members if x.bot])}", position = 2)

        # elif res.component.id == "stagechannel":
        #     allChannel = await category.create_stage_channel(name = f"총 멤버ㅣ {len(ctx.guild.members)}", position = 0)
        #     userChannel = await category.create_stage_channel(name = f"유저 수ㅣ {len([x for x in ctx.guild.members if not x.bot])}", position = 1)
        #     botChannel = await category.create_stage_channel(name = f"봇 수ㅣ {len([x for x in ctx.guild.members if x.bot])}", position = 2)

        # elif res.component.id == "voicechannel":
        #     allChannel = await category.create_voice_channel(name = f"총 멤버ㅣ {len(ctx.guild.members)}", position = 0)
        #     userChannel = await category.create_voice_channel(name = f"유저 수ㅣ {len([x for x in ctx.guild.members if not x.bot])}", position = 1)
        #     botChannel = await category.create_voice_channel(name = f"봇 수ㅣ {len([x for x in ctx.guild.members if x.bot])}", position = 2)
def setup(bot):
    bot.add_cog(management(bot))
