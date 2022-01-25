import io
import asyncio
from PycordPaginator import Paginator
import discord
from discord import colour
import discordSuperUtils
from discord.ext import commands
import aiosqlite
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


    async def cog_before_invoke(self, ctx: commands.Context):
        print(ctx.command)
        if ctx.command.name != '메일':
            database = await aiosqlite.connect("db/db.sqlite")
            cur = await database.execute(
                'SELECT * FROM uncheck WHERE user_id = ?', (ctx.author.id,)
            )

            if await cur.fetchone() is None:
                cur = await database.execute("SELECT * FROM mail")
                mails = await cur.fetchall()
                check = sum(1 for _ in mails)
                mal = discord.Embed(
                    title=f'📫짱구의 메일함 | {check}개 수신됨',
                    description="아직 읽지 않은 메일이 있어요.'`짱구야 메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                    colour=ctx.author.colour,
                )

                return await ctx.send(embed=mal)
            cur = await database.execute('SELECT * FROM mail')
            mails = await cur.fetchall()
            check = sum(1 for _ in mails)
            # noinspection DuplicatedCode
            cur = await database.execute("SELECT * FROM uncheck WHERE user_id = ?", (ctx.author.id,))
            # noinspection DuplicatedCode
            check2 = await cur.fetchone()
            if str(check) != str(check2[1]):
                mal = discord.Embed(
                    title=f'📫짱구의 메일함 | {int(check) - int(check2[1])}개 수신됨',
                    description="아직 읽지 않은 메일이 있어요.'`짱구야 메일`'로 확인하세요.\n주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                    colour=ctx.author.colour,
                )

                await ctx.send(embed=mal)

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
3️⃣|3. 유틸리티페이지 🧰
4️⃣|4. 게임페이지 🕹️
5️⃣|5. 음악 🎵
6️⃣|6. 도박 💴       
7️⃣|7. 생일 🎉
8️⃣|8. 학교검색 🏫
9️⃣|9. 방송 🎥


``문의는 봇DM으로 해주시면 감사합니다!``

[서포트서버](https://discord.gg/294KSUxcz2)
[짱구봇 초대](https://discord.com/api/oauth2/authorize?client_id=915546504054333450&permissions=8&scope=bot)
옵션&생일&입장메시지&레벨링&학교검색&방송&프리미엄&검색&애니&초대정보등의 코드는 팀에서 개발된 하린봇의 코드를 사용했음을 알려드립니다.
뮤직기능은 Wavelink기본 코드를 사용했음을 알려드립니다
[Wavelink](https://github.com/PythonistaGuild/Wavelink)
[하린봇깃헙](https://github.com/spacedev-official/harin)
``짱구야 하트인증``  한번씩해주세요!
        """,
        colour=discord.Colour.random()
        )
        main.set_thumbnail(url=self.bot.user.avatar_url)
        main.set_image(url="https://media.discordapp.net/attachments/921555509935480853/921555519578189834/c265877614d80026.png")
        main.set_footer(text=f"1 / 9페이지",icon_url=ctx.author.avatar_url)


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
        manage.add_field(name="짱구야 뮤직셋업",
                        value="```\n이 기능은 프리미엄기능이며 프리미엄을 \n구매하셔야 사용가능합니다 \n구매는 짱구봇 DM 일반문의로 넣어주세요\n```",
                        inline=False)
        manage.set_footer(text=f"2 / 9페이지",icon_url=ctx.author.avatar_url)


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
        utili.add_field(name="짱구야 봇정보",
                        value="```\n짱구봇 정보를 알려줘요\n```",
                        inline=False)
        utili.add_field(name="짱구야 옵션",
                        value="```\n여러 기능을 설정할 수 있는 명령어에요!\n```",
                        inline=False)
        utili.add_field(name="짱구야 애니 검색 [제목]",
                        value="```\n애니를 검색해 보세요!\n```",
                        inline=False)
        utili.add_field(name="짱구야 애니 댓글달기 [댓글내용]",
                        value="```\n애니 검색결과 메세지에 답장형태로 사용하여 댓글을 남겨요. \n부적절한 댓글은 무통보삭제가 되요.\n```",
                        inline=False)
        utili.add_field(name="짱구야 애니 댓글수정 [댓글내용]",
                        value="```\n애니 검색결과 메세지에 답장형태로 사용하여 댓글을 수정해요. \n부적절한 댓글은 무통보삭제가 되요.\n```",
                        inline=False)
        utili.add_field(name="짱구야 애니 댓글삭제",
                        value="```\n애니 검색결과 메세지에 답장형태로 사용하여 남긴 댓글을 삭제해요. \n부적절한 댓글은 무통보삭제가 되요.\n```",
                        inline=False)
        utili.add_field(
            name="짱구야 메일 (전체)",
            value="```\n전체 옵션을 사용하지않으면 수신된 메일을 보여주고 사용하면 모든 메일을 볼 수 있어요!\n```",
            inline=False
        )
        utili.add_field(
            name="짱구야 영화검색",
            value="```\n요번에 나온 영화를 검색해 보세요!\n```",
            inline=False
        )
        utili.add_field(
            name="짱구야 뉴스검색",
            value="```\n디스코드로 뉴스를 검색해 보세요!\n```",
            inline=False
        )
        utili.add_field(
            name="짱구야 카페검색",
            value="```\n네이버 카페를 검색해 보세요!\n```",
            inline=False
        )
        utili.add_field(
            name="짱구야 웹검색",
            value="```\n네이버등 웹사이트를 검색해 보세요!```",
            inline=False
        )
        utili.set_footer(text=f"3 / 9페이지",icon_url=ctx.author.avatar_url)

        games=discord.Embed(
            title="게임 🕹️",
            description="""
게임명령어를 사용해서
미니게임을 해보세요!
            """,
            colour=discord.Colour.random()
        )
        games.add_field(name="짱구야 가위바위보",
                        value="```\n가위바위보 게임\n```",
                        inline=False)
        games.add_field(name="짱구야 주사위",
                        value="```\n주사위를 돌려 누가 많이 나오는지 \n 내기를 해보세요!\n```",
                        inline=False)
        games.set_footer(text=f"4 / 9페이지",icon_url=ctx.author.avatar_url)

        music = discord.Embed(
            title="뮤직 🎶",
            description="""
                이곳에서 노래 관련 명령어를 확인해보세요!            
                """,
            colour=discord.Colour.random()
        )
        music.add_field(
            name="짱구야 들어와",
            value="```\n현재 접속한 음성채널에 접속해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 재생 인자값",
            value="```\n입력한 인자값(제목 또는 링크)을 불러와 재생해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 지금곡",
            value="```\n현재 재생중인 노래의 정보를 불러와요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 일시정지",
            value="```\n현재 재생중인 곡을 일시정지해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 이어재생",
            value="```\n일시정지된 곡을 이어서 재생해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 볼륨 (설정할볼륨)",
            value="```\n설정할 볼륨으로 볼륨을 조절해요. 입력하지 않으면 현재 볼륨을 보여줘요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 루프",
            value="```\n반복기능을 활성화하거나 비활성화해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 큐루프",
            value="```\n큐반복기능을 활성화하거나 비활성화해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 노래기록",
            value="```\n지금까지 재생됐던 노래기록을 불러와요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 정지",
            value="```\n현재 재생중인 곡을 완전히 정지해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 스킵",
            value="```\n현재 재생중인 곡을 스킵하거나 요청해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 큐",
            value="```\n현재 대기중인 큐목록을 보여줘요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 반복확인",
            value="```\n현재 설정된 반복상태를 보여줘요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 셔플",
            value="```\n셔플기능을 활성화하거나 비활성화해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 이전곡",
            value="```\n이전곡을 재생해요.\n```",
            inline=False
        )
        music.add_field(
            name="짱구야 나가",
            value="```\n현재 접속한 음성채널에서 노래를 멈추고 나가요.\n```",
            inline=False
        )
        music.set_footer(text=f"5 / 9페이지",icon_url=ctx.author.avatar_url)
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
        eco.add_field(name="짱구야 돈확인",
                    value="```\n도박시스템에 인벤토리를 확인합니다.\n```",
                    inline=False)
        eco.add_field(name="짱구야 입금 [돈]",
                    value="```\n통장에 돈을 넣으세요!\n```",
                    inline=False)
        eco.add_field(name="짱구야 출금 [돈]",
                    value="```\n통장에 돈을 빼세요!\n```",
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
        eco.add_field(name="짱구야 탈퇴 [돈]",
                    value="```\n도박을 해서 돈을 벌어보세요!\n```",
                    inline=False)
        eco.set_footer(text=f"6 / 9페이지",icon_url=ctx.author.avatar_url)
        birthday = discord.Embed(
            title="생일 🎉",
            description="""
                이곳에서 생일 관련 명령어를 확인해보세요!            
                """,
            colour=discord.Colour.random()
        )
        birthday.add_field(
            name="짱구야 생일등록",
            value="```\n자신의 생일을 등록해요.\n```",
            inline=False
        )
        birthday.add_field(
            name="짱구야 생일삭제",
            value="```\n등록된 자신의 생일을 삭제해요.\n```",
            inline=False
        )
        birthday.add_field(
            name="짱구야 생일 @유저맨션",
            value="```\n자신 혹은 지정한 유저의 생일을 조회해요.\n```",
            inline=False
        )
        birthday.add_field(
            name="짱구야 생일목록",
            value="```\n현재서버에 등록된 멤버들의 생일을 보여줘요.\n```",
            inline=False
        )
        birthday.set_footer(text=f"7 / 9페이지",icon_url=ctx.author.avatar_url)
        birthday = discord.Embed(
            title="생일 🎉",
            description="""
                이곳에서 생일 관련 명령어를 확인해보세요!            
                """,
            colour=discord.Colour.random()
        )
        birthday.add_field(
            name="짱구야 생일등록",
            value="```\n자신의 생일을 등록해요.\n```",
            inline=False
        )
        birthday.add_field(
            name="짱구야 생일삭제",
            value="```\n등록된 자신의 생일을 삭제해요.\n```",
            inline=False
        )
        birthday.add_field(
            name="짱구야 생일 (@user)",
            value="```\n자신 혹은 지정한 유저의 생일을 조회해요.\n```",
            inline=False
        )
        birthday.add_field(
            name="짱구야 생일목록",
            value="```\n현재길드에 등록된 멤버들의 생일을 보여줘요.\n```",
            inline=False
        )
        birthday.set_footer(text=f"5 / 8페이지",icon_url=ctx.author.avatar_url)

        school = discord.Embed(
            title="학교검색 🏫",
            description="""
                이곳에서 학교검색 관련 명령어를 확인해보세요!            
                """,
            colour=discord.Colour.random()
        )
        school.add_field(
            name="짱구야 학교검색 학교명",
            value="```\n학교의 정보를 조회해볼 수 있는 명령어에요!\n```",
            inline=False
        )
        school.add_field(
            name="짱구야 학교검색 급식 학교명",
            value="```\n학교급식을 조회해볼 수 있는 명령어에요!\n```",
            inline=False
        )
        school.set_footer(text=f"8 / 9페이지",icon_url=ctx.author.avatar_url)

        broadcast = discord.Embed(
            title="방송 🎥",
            description="트위치/유튜브 알림과 검색에 관련한 명령어를 확인해보세요.\n트위치/유튜브 알림 채널은 무료플랜은 1개, 프리미엄플랜은 5개까지 등록가능합니다.",
            colour=discord.Colour.random()
        )
        broadcast.add_field(
            name="짱구야 트위치",
            value="```\n트위치 스트리밍 알림 서비스에 등록된 채널 목록을 보여드려요.\n```",
            inline=False
        )
        broadcast.add_field(
            name="짱구야 트위치 등록 @알림역할 #알림채널 [유저ID]",
            value="```\n트위치 스트리밍 알림 서비스에 등록해요.\n```",
            inline=False
        )
        broadcast.add_field(
            name="짱구야 트위치 해제",
            value="```\n트위치 스트리밍 알림 서비스에서 해제해요.\n```",
            inline=False
        )
        broadcast.add_field(
            name="짱구야 유튜브 [채널이름]",
            value="```\n입력한 채널이름으로 검색해요.\n```",
            inline=False
        )
        broadcast.add_field(
            name="짱구야 유튜브 등록 @알림역할 #알림채널 [채널ID]",
            value="```\n유튜브 업로드 알림 서비스에 등록해요.\n```",
            inline=False
        )
        broadcast.add_field(
            name="짱구야 유튜브 해제",
            value="```\n유튜브 업로드 알림 서비스에서 해제해요.\n```",
            inline=False
        )
        broadcast.set_footer(text="9 / 9페이지", icon_url=ctx.author.avatar_url)
        desc = {
            "메인 페이지": "메뉴가 있는 메인페이지",
            "서버 관리 🔰": "서버 관리 명령어가 있는 페이지.",
            "유틸리티 🧰":"유틸리티 명령어가 있는 페이지",
            "게임 🕹️":"게임 명령어가 있는 페이지",
            "음악 🎵":"음악 명령어가 있는 페이지",
            "도박 💴":"도박 명령어가 있는 페이지",
            "생일 🎉": "생일 명령어가 있는 페이지",
            "학교검색 🏫":"트위치/유튜브 명령어가 있는페이지",
            "방송 🎥":"트위치/유튜브 명령어가 있는페이지",
        }

        embeds = [main,manage,utili,games,music,eco,birthday,broadcast,school]
        e = Paginator(
            client=self.bot.components_manager,
            embeds=embeds,
            channel=ctx.channel,
            only=ctx.author,
            ctx=ctx,
            use_select=True,
            desc=desc)
        await e.start()
        
    @commands.command(name="메일", help="`짱구야 메일 (전체)`로 메일을 확인합니다.")
    async def read_mail(self, ctx, mode=None):
        if mode is None:
            dictcommand = await self.read_email_from_db(ctx=ctx)
            database = dictcommand["database"]
            contents = dictcommand["contents"]
            cur = dictcommand["cur"]
            uncheck_cur = dictcommand["uncheck_cur"]
            timess = dictcommand["timess"]
            pages = dictcommand["pages"]
            check2 = await cur.fetchone()
            uncheck_cur_fetchone = await uncheck_cur.fetchone()
            if uncheck_cur_fetchone is None:
                await database.execute("INSERT INTO uncheck VALUES (?, ?)", (ctx.author.id, str(pages)))
                await database.commit()
                mal = discord.Embed(title=f"📫짱구의 메일함 | {str(pages)}개 수신됨",
                                    description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                    colour=ctx.author.colour)
                cur_page = 1
            else:
                if str(pages) == str(uncheck_cur_fetchone[1]):
                    mal = discord.Embed(title=f"📫짱구의 메일함 | 수신된 메일이 없어요.",
                                        description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                        colour=ctx.author.colour)
                    mal.add_field(name="📭빈 메일함", value="✅모든 메일을 읽으셨어요. 전체메일을 보고싶으시면 `짱구야 메일 전체`를 입력하세요.")
                    return await ctx.send(embed=mal)
                await database.execute("UPDATE uncheck SET check_s = ? WHERE user_id = ?",
                                       (str(pages), ctx.author.id))
                await database.commit()
                mal = discord.Embed(title=f"📫짱구의 메일함 | {pages - int(uncheck_cur_fetchone[1])}개 수신됨",
                                    description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                    colour=ctx.author.colour)
                cur_page = int(uncheck_cur_fetchone[1])
            # noinspection DuplicatedCode
            mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                          value=contents[cur_page - 1])
            message = await ctx.send(embed=mal)
            # getting the message object for editing and reacting

            await message.add_reaction("◀️")
            await message.add_reaction("▶️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"] and reaction.message.id == message.id

            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                    # waiting for a reaction to be added - times out after x seconds, 60 in this
                    # example

                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        if check2 is None:
                            cur_page += 1
                            mal = discord.Embed(title=f"📫짱구의 메일함 | {str(pages)}개 수신됨",
                                                description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                                colour=ctx.author.colour)
                            mal.add_field(name=f"{pages}중 {cur_page}번째 메일", value=contents[cur_page - 1])
                        else:
                            cur_page += 1
                            mal = discord.Embed(title=f"📫짱구의 메일함 | {pages - int(uncheck_cur_fetchone[1])}개 수신됨",
                                                description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                                colour=ctx.author.colour)
                            mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                                          value=contents[cur_page - 1])
                        await message.edit(embed=mal)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        if check2 is None:
                            cur_page -= 1
                            mal = discord.Embed(title=f"📫짱구의 메일함 | {str(pages)}개 수신됨",
                                                description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                                colour=ctx.author.colour)
                            mal.add_field(name=f"{pages}중 {cur_page}번째 메일", value=contents[cur_page - 1])
                        else:
                            cur_page -= 1
                            mal = discord.Embed(title=f"📫짱구의 메일함 | {pages - int(uncheck_cur_fetchone[1])}개 수신됨",
                                                description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                                colour=ctx.author.colour)
                            mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                                          value=contents[cur_page - 1])
                        await message.edit(embed=mal)
                except asyncio.TimeoutError:
                    break
        elif mode == "전체":
            dictcommand = await self.read_email_from_db(ctx=ctx)
            contents = dictcommand["contents"]
            timess = dictcommand["timess"]
            pages = dictcommand["pages"]
            mal = discord.Embed(title=f"📫짱구의 메일함",
                                description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                colour=ctx.author.colour)
            cur_page = 1
            # noinspection DuplicatedCode
            mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                          value=contents[cur_page - 1])
            message = await ctx.send(embed=mal)

            await message.add_reaction("◀️")
            await message.add_reaction("▶️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"] and reaction.message.id == message.id
                # This makes sure nobody except the command sender can interact with the "menu"

            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                    # waiting for a reaction to be added - times out after x seconds, 60 in this
                    # example

                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        cur_page += 1
                        mal = discord.Embed(title=f"📫짱구의 메일함",
                                            description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                            colour=ctx.author.colour)
                        mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                                      value=contents[cur_page - 1])
                        await message.edit(embed=mal)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        cur_page -= 1
                        mal = discord.Embed(title=f"📫짱구의 메일함",
                                            description="주기적으로 메일함을 확인해주세요! 소소한 업데이트 및 이벤트개최등 여러소식을 확인해보세요.",
                                            colour=ctx.author.colour)
                        mal.add_field(name=f"{pages}중 {cur_page}번째 메일({timess[contents[cur_page - 1]]}작성)",
                                      value=contents[cur_page - 1])
                        await message.edit(embed=mal)
                except asyncio.TimeoutError:
                    break

    @staticmethod
    async def read_email_from_db(ctx):
        contents = []
        timess = {}
        database = await aiosqlite.connect("db/db.sqlite")
        cur = await database.execute('SELECT * FROM mail')
        uncheck_cur = await database.execute('SELECT * FROM uncheck WHERE user_id = ?',(ctx.author.id,))
        mails = await cur.fetchall()
        for i in mails:
            contents.append(i[1])
            timess[i[1]] = i[2]
        pages = len(contents)
        return {"contents": contents, "timess": timess, "database": database, "cur": cur, "uncheck_cur":uncheck_cur, "pages": pages}
def setup(bot):
    bot.add_cog(help(bot))