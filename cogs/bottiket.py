import discord
from discord import embeds
from discord.ext import commands

import os
from discord.ext.commands.core import command
import pytz
import datetime

ticket_guild_id = 915551354800451616
category_id = 915561810411814973
close_ticket_category_id = 915561835267231774
# 오류 ~~~~ 37라인

class question(commands.Cog): # 야이 미친놈아 command.Cog가 뭐냐
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ctx = await self.bot.get_context(message)
        if message.author.bot:
            return
        # if message.content.startswith(["!", "#", "/", self.bot.command_prefix[0]]):
        #     return
        if message.content.startswith("!") or message.content.startswith("#") or message.content.startswith("/") or message.content.startswith(self.bot.command_prefix[0]):
            return

        if str(message.channel.type) in "private":
            ticket_guild = self.bot.get_guild(ticket_guild_id)
            _lambda = list(
                filter(
                    lambda x: x.topic == str(ctx.author.id), ticket_guild.text_channels
                )
            )
            if _lambda:
                i = _lambda[0]
                if message.content == None: #?
                    if message.attachments:
                        lists = list(
                            map(
                                lambda attachment: f"[클릭해서 보기]({attachment.proxy_url})",
                                message.attachments,
                            )
                        )
                        await i.send(
                            embed=discord.Embed(
                                descripiton="(첨부파일을 보냈습니다)\n\n" + "\n".join(lists)
                            ).set_author(
                                icon_url=ctx.author.avatar_url,
                                name=f"{ctx.author} ({ctx.author.id})",
                            )
                        )
                        await message.add_reaction("✅")
                    elif message.stickers:
                        await i.send(
                            embed=discord.Embed(description="(스티커를 보냈습니다)")
                            .set_thumbnail(url=message.stickers[0].image_url)
                            .set_author(
                                icon_url=ctx.author.avatar_url,
                                name=f"{ctx.author} ({ctx.author.id})",
                            )
                        )
                        await message.add_reaction("✅")
                    else:
                        await i.send(
                            embed=discord.Embed(
                                description="(핸들링 되지 않은 메시지를 보냈습니다.)"
                            ).set_author(
                                icon_url=ctx.author.avatar_url,
                                name=f"{ctx.author} ({ctx.author.id})",
                            )
                        )
                        await message.add_reaction("✅")
                else:
                    await i.send(
                        embed=discord.Embed(description=message.content).set_author(
                            icon_url=ctx.author.avatar_url,
                            name=f"{ctx.author} ({ctx.author.id})",
                        )
                    )
                    await message.add_reaction("✅")
            else:
                if message.author.bot:
                    return
                open_ticket_category = ticket_guild.get_channel(category_id) # 이건 왜 길드 아이디지
                new_ticket = await message.author.send(
                            embed = discord.Embed(
                            title=f'문의',
                            description =f"문의를 해주셔서 감사힙니다. \n 답변이 늦을수도 있으니 \n 기다려주세요.\n \n \n **:warning:  주의사항** \n \n `` 불필요한 문의는 제재 됩니다.`` \n \n ``관리자를 욕할시 처벌대상이 됩니다.`` \n \n ``관리자를 존중해주세요.``" ,
                            colour = discord.Colour.blue(),
                        ).set_thumbnail(url="https://cdn.discordapp.com/avatars/872714206246469662/810ef9d933f9985d82f441de0a03fb6b.webp?size=80")
                )

                ticket_channel = await open_ticket_category.create_text_channel(
                    message.author.dm_channel.id,
                    topic=f"{message.author.id}",
                    position = 1
                )
                staff = ticket_guild.get_role(857395557793792020) # 이건 안넣냐
                await ticket_channel.set_permissions(
                    staff,
                    read_messages=True,
                    send_messages=True,
                    read_message_history=True,
                )
                await ticket_channel.send(
                    embed=discord.Embed(description=message.content).set_author(
                        icon_url=ctx.author.avatar_url,
                        name=f"{ctx.author} ({ctx.author.id})",
                    )
                )
                await message.add_reaction("✅")
        elif str(message.channel.type) != "private":
            try:
                if message.channel.category.id == category_id:
                    await (await self.bot.fetch_user(int(message.channel.topic))).send(
                        embed=discord.Embed(
                            title="** 문의 답변 **",
                            description=f"**`관리자` {message.author.name}** : `{message.content}",
                            colour = discord.Colour.blue(),
                            )
                        )
                    await message.add_reaction("✅")
            except:
                pass

    @commands.command(name="문의종료", aliases=["종료", "close"])
    @commands.has_permissions(administrator=True)
    async def ticket_end(self, ctx):
        await ctx.message.delete()
        ticket_guild = self.bot.get_guild(ticket_guild_id)
        ticket_channel = self.bot.get_channel(ctx.channel.id)
        await (await self.bot.fetch_user(int(ctx.channel.topic))).send(
            embed = discord.Embed(title=f'문의',
            description =f"**문의종료**\n  문의를 종료하겠습니다 문의를 해주셔서 감사합니다.",
            colour = discord.Colour.blue(),
            ).set_thumbnail(url="https://cdn.discordapp.com/avatars/872714206246469662/810ef9d933f9985d82f441de0a03fb6b.webp?size=80")
            
        )
        await ctx.channel.edit(
            topic="close-{}".format(ctx.channel.name),
            category=ticket_guild.get_channel(close_ticket_category_id),
            position = len(ctx.channel.category.channels)
        )
        await ctx.channel.edit(
            name = ctx.channel.topic
        )
        embed = discord.Embed(
            colour=0xFF00, title="문의종료", description=f"잠금 요청 유저 : {ctx.author}"
        )
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(question(bot))
