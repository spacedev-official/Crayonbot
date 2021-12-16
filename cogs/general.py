import io
import asyncio
import discord
import random
import asyncio
import random
import datetime
import config
import discord
from discord import errors
from discord.ext import commands
from discord.ext import commands
class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "핑"
    )
    async def ping(self, ctx):
        await ctx.send(embed = discord.Embed(title = "**Pong!**", description = f":ping_pong: {round(self.bot.latency) * 1000}ms", color= 0x0000ff))
    @commands.command(name="출처")
    async def chul(self, ctx):
        embed=discord.Embed(name="깃헙", dscription=f"""
[서포트서버](https://discord.gg/Jk6VRvsnqa)
[짱구봇 초대](https://discord.com/api/oauth2/authorize?client_id=915546504054333450&permissions=8&scope=bot)
옵션&생일&입장메시지&레벨링&초대정보&하트인증등의 코드는 팀에서 개발된 하린봇의 코드를 사용했음을 알려드립니다.
[하린봇깃헙](https://github.com/spacedev-official/harin)        
        """, colour=discord.Colour.random)
        await ctx.reply(embed=embed)
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild.owner.id == 898755879766204416:
            return await guild.leave()
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(name="짱구야 도움 | 서버: {}".format(len(self.bot.guilds)),
                                                                 type=discord.ActivityType.playing))
        if guild.id in [653083797763522580, 786470326732587008, 608711879858192479]:
            return
        em = discord.Embed(
            title="초대해줘서 고마워요!",
            description="""
짱구봇을 초대주셔서 감사드립니다.
짱구봇은 유저 친화적이며 다기능봇입니다.
도움말은 `짱구야 도움`,
프리픽스는 `짱구야 `,`짱구야`,`ㄱ `,`ㄱ` 입니다.            
"""
        )
        em.set_thumbnail(url=self.bot.user.avatar_url)
        em.set_image(
            url="https://cdn.discordapp.com/attachments/915556934977998879/917754253701951499/c265877614d80026.png")
        try:
            await guild.owner.send(embed=em)
        except errors.HTTPException:  # errors.Forbidden when does not have permission
            # except error as error mean except (error, error) <- does not working in python 3.10
            ch = self.bot.get_channel((random.choice(guild.channels)).id)
            await ch.send(embed=em)
        em = discord.Embed(
            description=f"{guild.name}({guild.id})에 접속함\n서버수 : {len(self.bot.guilds)}"
        )
        await self.bot.get_channel(915551578730164234).send(embed=em)
    @commands.command(name="출처")
    async def chul(self, ctx):
        embed=discord.Embed(name="깃헙", dscription=f"""
[서포트서버](https://discord.gg/Jk6VRvsnqa)
[짱구봇 초대](https://discord.com/api/oauth2/authorize?client_id=915546504054333450&permissions=8&scope=bot)
옵션&생일&입장메시지&레벨링&초대정보등의 코드는 팀에서 개발된 하린봇의 코드를 사용했음을 알려드립니다.
[하린봇깃헙](https://github.com/spacedev-official/harin)        
        """, colour=discord.Colour.random)
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(name="짱구야 도움 | 서버: {}".format(len(self.bot.guilds)),
                                                                 type=discord.ActivityType.playing))
        em = discord.Embed(
            description=f"{guild.name}({guild.id})에서 나감\n서버수 : {len(self.bot.guilds)}"
        )
        await self.bot.get_channel(915551578730164234).send(embed=em)
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        embed=discord.Embed(title="메시지수정로그", color=0x00FFFF)
        embed.set_footer(text=f"멤버 이름 :{before.author.name} • Message ID: {before.id}")
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name='수정전:', value=before.content , inline=False)
        embed.add_field(name="수정후:", value=after.content , inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/915551354800451616/f27061c35e3f1dc203b3564cd864e99a.webp?size=96")        
        channel = self.bot.get_channel(915555627332435988)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(title="메시지 삭제로그", color= 0x0000ff)
        embed.add_field(name="**메시지삭제**", value=f"메시지 : {message.content} \n \n 삭제됨")
        embed.set_thumbnail(url="https://cdn.discordapp.com/icons/915551354800451616/f27061c35e3f1dc203b3564cd864e99a.webp?size=96")
        embed.timestamp = datetime.datetime.utcnow()
        embed.colour = (0x000ff)
        dele = self.bot.get_channel(915555627332435988)
        await dele.send(embed=embed)

    #에러로그
    @commands.Cog.listener()
    async def on_command(self, ctx):
       self.logger.info(f"{ctx.author}({ctx.author.id}) - {ctx.message.content}")
       await self.bot.get_channel(int(config.BotSettings.logging_channel)).send(f"{ctx.author}({ctx.author.id}) - `{ctx.message.content}`")
       await self.bot.get_channel(int(config.BotSettings.stafflog)).send(f"{ctx.author}({ctx.author.id}) - `{ctx.message.content}`")
    #일반로그
    @commands.Cog.listener()
    async def on_command(self, ctx):
        channel = self.bot.get_channel(915555649990053918)
        embed = discord.Embed(
            title ="일반로그",
            description= f"닉네임 : {ctx.author} \n \n 아이디 : {ctx.author.id} \n \n 명령어로그 : {ctx.message.content}",
            color= 0x0000ff
        ).set_thumbnail(url="https://cdn.discordapp.com/icons/915551354800451616/f27061c35e3f1dc203b3564cd864e99a.webp?size=96")        
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)
def setup(bot):
    bot.add_cog(general(bot))
