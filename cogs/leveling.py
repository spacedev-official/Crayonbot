import aiosqlite
import discord
from discord.ext import commands

import discordSuperUtils


class Leveling(commands.Cog, discordSuperUtils.CogManager.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.LevelingManager = discordSuperUtils.LevelingManager(bot, award_role=False)
        self.ImageManager = discordSuperUtils.ImageManager()
        super().__init__()  # Make sure you define your managers before running CogManager.Cog's __init__ function.
        # Incase you do not, CogManager.Cog wont find the managers and will not link them to the events.
        # Alternatively, you can pass your managers in CogManager.Cog's __init__ function incase you are using the same
        # managers in different files, I recommend saving the managers as attributes on the bot object, instead of
        # importing them.

    
    # noinspection PyUnusedLocal
    @discordSuperUtils.CogManager.event(discordSuperUtils.LevelingManager)
    async def on_level_up(self, message, member_data, roles):
        if message.guild.id in [653083797763522580, 786470326732587008]:
            return
        if not str(message.channel.topic).find("-HNoLv") != -1:
            await message.reply(
                f"🆙축하합니다! `{await member_data.level()}`로 레벨업 하셨어요!🆙"
            )

    @commands.command(name="랭크", aliases=["레벨"])
    async def rank(self, ctx, member: discord.Member = None):
        database = self.bot.db
        await self.LevelingManager.connect_to_database(
            database, ["xp", "roles", "role_list"]
        )
        mem_obj = member or ctx.author
        member_data = await self.LevelingManager.get_account(mem_obj)

        if not member_data:
            await ctx.send('정보를 만들고있어요! 조금만 기다려주세요!😘')
            return

        guild_leaderboard = await self.LevelingManager.get_leaderboard(ctx.guild)
        member = [x for x in guild_leaderboard if x.member == mem_obj]
        member_rank = guild_leaderboard.index(member[0]) + 1 if member else -1

        image = await self.ImageManager.create_leveling_profile(
            member=mem_obj,
            member_account=member_data,
            background=discordSuperUtils.Backgrounds.GALAXY,
            # name_color=(255, 255, 255),
            # rank_color=(127, 255, 0),
            # level_color=(255, 255, 255),
            # xp_color=(255, 255, 255),
            # bar_outline_color=(255, 255, 255),
            # bar_fill_color=(127, 255, 0),
            # bar_blank_color=(72, 75, 78),
            # profile_outline_color=(100, 100, 100),
            rank=member_rank,
            font_path="user.ttf",
            outline=5,
        )

        await ctx.send(file=image)

    @commands.command(name="리더보드")
    async def leaderboard(self, ctx):
        guild_leaderboard = await self.LevelingManager.get_leaderboard(ctx.guild)
        formatted_leaderboard = [
            f"멤버: {x.member}, XP: {await x.xp()}" for x in guild_leaderboard
        ]

        await discordSuperUtils.PageManager(
            ctx,
            discordSuperUtils.generate_embeds(
                formatted_leaderboard,
                title="레벨 리더보드",
                fields=25,
                description=f"{ctx.guild}의 순위판!",
            ),
        ).run()

def setup(bot):
    bot.add_cog(Leveling(bot))
