import io
import asyncio
from PycordPaginator import Paginator
import discord
from discord import colour
import discordSuperUtils
from discord.ext import commands

from cogs.util import util
# 1️⃣ 키캡 디지트 원
# 2️⃣ 키캡 숫자 2
# 3️⃣ 키캡 숫자 3
# 4️⃣ 키캡 숫자 4
# 5️⃣ 키캡 숫자 5
# 6️⃣ 키캡 숫자 6
# 7️⃣ 키캡 디지트 세븐
# 8️⃣ 키캡 숫자 8
# 9️⃣ 키캡 숫자 나인
# 🔟 키캡 : 10


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()


    
    @commands.command(name="도움말", aliases=['도움'])
    async def pagination(self, ctx):
        global embeds
        main = discord.Embed(
            title = "메인",
            description="""
안녕하세요! 짱구봇을 사용해주셔서 감사합니다!

도움말 메뉴는 아래와 같습니다

1️⃣|1. 메인페이지
2️⃣|2. 서버관리페이지 🔰 
3️⃣|3. 코로나페이지 🧬
4️⃣|4. 유틸리티페이지 🧰
5️⃣|5. 게임페이지 🕹️
6️⃣|6. 음악 🎵
7️⃣|7. 도박 💴       


``문의는 봇DM으로 해주시면 감사합니다!``

[서포트서버](https://discord.gg/Jk6VRvsnqa)
[짱구봇 초대](https://discord.com/api/oauth2/authorize?client_id=915546504054333450&permissions=8&scope=bot)
옵션&생일&입장메시지&레벨링&초대정보등의 코드는 팀에서 개발된 하린봇의 코드를 사용했음을 알려드립니다.
[하린봇깃헙](https://github.com/spacedev-official/harin)
            
        """,
        colour=discord.Colour.random()
        )
        main.set_footer(text=f"1 / 7페이지",icon_url=ctx.author.avatar_url)


        manage = discord.Embed(
            title="서버 관리 🔰",
            description="""
서버관리 명령어를 사용해보세요!     
모든 관리명령어는 관리자 권한을
가진 사람들만 사용할수 있습니다.
""",
            colour=discord.Colour.random()
        )
        manage.add_field(name="짱구야 추방 @유저 [사유]",
                         value="```\n맨션된 유저를 추방을 해요\n```",
                         inline=False)
        manage.add_field(name="짱구야 밴 @유저 [사유]",
                         value="```\n맨션된 유저를 차단을 해요\n```",
                         inline=False)
        manage.add_field(name="짱구야 언밴 @유저",
                         value="```\n맨션된 유저를 언밴을 해요\n```",
                         inline=False)
        manage.add_field(name="짱구야 뮤트 @유저",
                         value="```\n맨션된 유저를 뮤트를 해요\n```",
                         inline=False)
        manage.add_field(name="짱구야 언뮤트 @유저",
                         value="```\n맨션된 유저를 언뮤트을 해요\n```",
                         inline=False)
        manage.add_field(name="짱구야 서버공지 [작성]",
                         value="```\n자신의 서버에 공지를 올려요!\n```",
                         inline=False)
        manage.add_field(name="짱구야 청소 [갯수]",
                         value="```\n메시지를 청소를 해요!\n```",
                         inline=False)
        manage.add_field(name="짱구야 티켓설정 [#티켓채널] [@지원팀역할] [티켓안내내용]",
                        value="```\n티켓을 설정해서 문의를 받아보세요!\n```",
                        inline=False)
        manage.set_footer(text=f"2 / 7페이지",icon_url=ctx.author.avatar_url)


        utili = discord.Embed(
            title="유틸리티 🧰",
            description="""
유틸리티 명령어를 사용해보세요!

  
            """,
            colour=discord.Colour.random()
        )
        utili.add_field(name="짱구야 유저정보 @유저",
                        value="```\n맨션한 유저정보를 보여줍니다\n```",
                        inline=False)
        utili.add_field(name="짱구야 내정보",
                        value="```\n당신의 정보를 보여줍니다\n```",
                        inline=False)
        utili.add_field(name="짱구야 서버정보",
                        value="```\n지금 있는 서버정보를 보여줍니다\n```",
                        inline=False)
        utili.add_field(name="짱구야 프사",
                        value="```\n당신의 프사를 보여줍니다\n```",
                        inline=False)
        utili.add_field(name="짱구야 프사 @유저",
                        value="```\n맨션한 유저의 프사를 보여줍니다\n```",
                        inline=False)
        utili.add_field(name="짱구야 [랭크 or 레벨] (@user)",
                        value="```\n맨션한 유저의 랭크를 보여줍니다\n```",
                        inline=False)
        utili.add_field(name="짱구야 리더보드",
                        value="```\n현재 서버의 레벨순위정보판을 보여드려요.\n```",
                        inline=False)
        utili.add_field(name="짱구야 초대정보 @유저",
                        value="```\n지정한 유저 혹은 자신의 초대정보를 보여줘요.\n```",
                        inline=False)
        utili.add_field(name="짱구야 옵션",
                        value="```\n여러 기능을 설정할 수 있는 명령어에요!\n```",
                        inline=False)
        
        utili.set_footer(text=f"4 / 7페이지",icon_url=ctx.author.avatar_url)

        games=discord.Embed(
            title="게임 🕹️",
            description="""
게임명령어를 사용해서
미니게임을 해보세요!
            """,
            colour=discord.Colour.random()
        )
        games.add_field(name="천상아 가위바위보",
                        value="```\n가위바위보 게임\n```",
                        inline=False)
        games.add_field(name="천상아 주사위",
                        value="```\n주사위를 돌려 누가 많이 나오는지 \n 내기를 해보세요!\n```",
                        inline=False)
        games.set_footer(text=f"5 / 7페이지",icon_url=ctx.author.avatar_url)

        music=discord.Embed(
            title="음악 🎵",
            description="""
노래명령어를 사용해보세요!
            """,
            colour=discord.Colour.random()
        )
        music.add_field(
            name="짱구야 들어와",
            value="```\n현재 접속한 음성채널에 접속해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 재생 [인지값]",
            value="```\n입력한 인자값(제목 또는 링크)을 불러와 재생해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 일시정지",
            value="```\n현재 재생중인 곡을 일시정지해요\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 현재곡",
            value="```\n현재 재생중인 노래의 정보를 불러와요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 스킵",
            value="```\n현재 재생중인 곡을 스킵해요\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 볼륨 (설정할볼륨)",
            value="```\n설정할 볼륨으로 볼륨을 조절해요. 입력하지 않으면 현재 볼륨을 보여줘요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 재생목록",
            value="```\n재생목록을 확인해요\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 셔플",
            value="```\n셔플기능을 활성화하거나 비활성화해요.\n```",
            inline=False
        )
        music.set_footer(text=f"6 / 7페이지",icon_url=ctx.author.avatar_url)
        eco=discord.Embed(
            title="도박 💴",
            description="""
도박명령어를 사용해보세요!
            """,
            colour=discord.Colour.random()
        )
        eco.add_field(name="짱구야 가입",
                    value="```\n도박시스템에 가입을합니다.\n```",
                    inline=False)
        eco.add_field(name="짱구야 인벤",
                    value="```\n도박시스템에 인벤토리를 확인합니다.\n```",
                    inline=False)
        eco.add_field(name="짱구야 구입 [이름]",
                    value="```\n상품을 구입을 가능합니다.\n```",
                    inline=False)
        eco.add_field(name="짱구야 목록",
                    value="```\n상품 목록을 확인합니다!\n```",
                    inline=False)
        eco.add_field(name="짱구야 송금 [유저맨션] [돈]",
                    value="```\n맨션된 유저한테 돈을 보냅니다.\n```",
                    inline=False)
        eco.add_field(name="짱구야 지원금",
                    value="```\n일정 쿨타임마다 지원금을 받을수 있습니다.\n```",
                    inline=False)
        eco.add_field(name="짱구야 도박 [돈]",
                    value="```\n도박을 해서 돈을 벌어보세요!\n```",
                    inline=False)
        eco.set_footer(text=f"7 / 7페이지",icon_url=ctx.author.avatar_url)
        desc = {
            "메인 페이지": "메뉴가 있는 메인페이지",
            "서버 관리 🔰": "서버 관리 명령어가 있는 페이지.",
            "유틸리티 🧰":"유틸리티 명령어가 있는 페이지",
            "게임 🕹️":"게임 명령어가 있는 페이지",
            "음악 🎵":"음악 명령어가 있는 페이지",
            "도박 💴":"도박 명령어가 있는 페이지",
        }

        embeds = [main,manage,utili,games,music,eco]
        e = Paginator(
            client=self.bot.components_manager,
            embeds=embeds,
            channel=ctx.channel,
            only=ctx.author,
            ctx=ctx,
            use_select=True,
            desc=desc)
        await e.start()

def setup(bot):
    bot.add_cog(help(bot))
