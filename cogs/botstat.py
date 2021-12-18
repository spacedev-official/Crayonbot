import asyncio
import os
import random
import aiosqlite
from dotenv import load_dotenv
import discord
from discord import errors
from discord.ext import commands
import koreanbots
from koreanbots.integrations import discord
load_dotenv(verbose=True)
class botstat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.krb = koreanbots.Koreanbots(api_key=os.getenv("KRB_TOKEN"))
        self._krb = discord.DiscordpyKoreanbots(client=self.bot,api_key=os.getenv("KRB_TOKEN"),run_task=True)

    @commands.command(name="하트인증", aliases=["추천인증","추천","하트","ㅊㅊ"])
    async def heart_check(self,ctx):
        voted = await self.krb.is_voted(user_id=ctx.author.id,bot_id=self.bot.user.id)
        if voted.voted:
            return await ctx.reply("> 하트를 해주셔서 감사해요!💕")
        msg = await ctx.reply("> 하트를 하지 않으신 것 같아요.. 아래링크로 이동하셔서 하트를 해주세요!\n> 링크: https://koreanbots.dev/bots/915546504054333450/vote\n> 1분후 재확인 할게요!")
        await asyncio.sleep(60)
        voted = await self.krb.is_voted(user_id=ctx.author.id, bot_id=self.bot.user.id)
        if voted.voted:
            return await msg.edit("> 하트 확인되었어요! 하트를 해주셔서 감사해요!💕")
        await msg.edit("> 하트가 확인되지않았어요..😢 혹시 마음에 드시지않으신가요..?🥺")

def setup(bot):
    bot.add_cog(botstat(bot))
