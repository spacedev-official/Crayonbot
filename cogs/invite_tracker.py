import aiosqlite
import discord
import discordSuperUtils
from discord.ext import commands


class InviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()
        self.InviteTracker = discordSuperUtils.InviteTracker(self.bot)

    @commands.Cog.listener("on_member_join")
    async def invite_tracker(self, member):
        database_one = await aiosqlite.connect("db/db.sqlite")
        database = discordSuperUtils.DatabaseManager.connect(database_one)
        await self.InviteTracker.connect_to_database(database, ["invites"])
        cur = await database_one.execute("SELECT * FROM invite_tracker WHERE guild = ?", (member.guild.id,))
        data = await cur.fetchone()
        if data is not None:
            invite = await self.InviteTracker.get_invite(member)
            inviter = await self.InviteTracker.fetch_inviter(invite)
            await self.InviteTracker.register_invite(invite, member, inviter)

            channel = self.bot.get_channel(data[1])
            await channel.send(
                f"{member.mention}님은 {inviter.display_name if inviter else '알수없는 사용자'}님의 초대로 오셨어요! 코드 - {invite.code}"
            )

    @commands.command(name="초대정보")
    async def info(self, ctx, member: discord.Member = None):
        database_one = await aiosqlite.connect("db/db.sqlite")
        database = discordSuperUtils.DatabaseManager.connect(database_one)
        await self.InviteTracker.connect_to_database(database, ["invites"])
        member = ctx.author if not member else member
        invited_members = await self.InviteTracker.get_user_info(member).get_invited_users()

        await ctx.send(
            f"{member.mention}님이 초대한 멤버들({len(invited_members)}명): "
            + ", ".join(str(x) for x in invited_members)
        )


def setup(bot):
    bot.add_cog(InviteTracker(bot))
