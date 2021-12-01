import aiosqlite
import discordSuperUtils
from discord.ext import commands
import emoji

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()

    @commands.Cog.listener("on_member_join")
    async def member_welcome(self, member):
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute("SELECT * FROM welcome WHERE guild = ?", (member.guild.id,))
        data = await cur.fetchone()
        if data is not None:
            img = await self.ImageManager.create_welcome_card(
                member,
                "https://media.discordapp.net/attachments/885113533300367390/915548254127669269/1d2958f6ae79a237.jpg",
                # discordSuperUtils.Backgrounds.DISCORD,#discordSuperUtils.ImageManager.load_asset("bgimg.png")
                f"어서오세요!, {member}님!",
                "서버 법률을 확인해주시고 많은 이용부탁드립니다!",
                title_color=(127, 255, 0),
                description_color=(127, 255, 0),
                font_path="user.ttf"
            )
            channel = self.bot.get_channel(data[1])
            await channel.send(f"<a:17:905521904272687135> 반가워요 {member.mention} 님 저희 𝓦𝓸𝓻𝓵𝓭는 <a:17:905521904272687135>\n \n<a:13:905521904775987220>  재밌게 게임하며 친목을 유지하는 서버입니다. <a:13:905521904775987220> \n \n<a:52:905521905136705566>  저희 서버 법률은 <#905112849410555971> 에서 숙지해주세요 <a:73:905521905228988417>\n \n<:41:905521905119924234> 아! 그리고 <#905112849410555966> 에서 인증해주시고 <:41:905521905119924234> \n \n<a:33:905521905090560031> <#905992216298803282> 에서 자기소개 써주세용~~! <a:33:905521905090560031> ",file=img)


def setup(bot):
    bot.add_cog(Welcome(bot))
