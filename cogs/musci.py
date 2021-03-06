import datetime
import time
from typing import Optional

import aiosqlite
import discord
import discordSuperUtils
from discord.ext import commands
from discordSuperUtils import MusicManager


# Format duration
def parse_duration(duration: Optional[float]) -> str:
    return (
        time.strftime("%H:%M:%S", time.gmtime(duration))
        if duration != "LIVE"
        else duration
    )


# Format view count
# noinspection DuplicatedCode
def parse_count(count):
    original_count = count

    count = float("{:.3g}".format(count))
    magnitude = 0
    matches = ["", "K", "M", "B", "T", "Qua", "Qui"]

    while abs(count) >= 1000:
        if magnitude >= 5:
            break

        magnitude += 1
        count /= 1000.0

    try:
        return "{}{}".format(
            "{:f}".format(count).rstrip("0").rstrip("."), matches[magnitude]
        )
    except IndexError:
        return original_count


class Music(commands.Cog, discordSuperUtils.CogManager.Cog, name="Music"):
    def __init__(self, bot):
        self.bot = bot
        self.skip_votes = {}  # Skip vote counter dictionary

        # self.client_secret = "" # spotify client_secret
        # self.client_id = "" # spotify client_id

        # Get your's from here https://developer.spotify.com/

        self.MusicManager = MusicManager(self.bot, spotify_support=False)

        # self.MusicManager = MusicManager(bot,
        #                                  client_id=self.client_id,
        #                                  client_secret=self.client_secret,
        #                                  spotify_support=True)

        # If using spotify support use this instead ^^^

        self.ImageManager = discordSuperUtils.ImageManager()
        super().__init__()

    # noinspection DuplicatedCode

    # Play function
    async def play_cmd(self, ctx, query):
        async with ctx.typing():
            player = await self.MusicManager.create_player(query, ctx.author)

        if player:
            if not ctx.voice_client or not ctx.voice_client.is_connected():
                await self.MusicManager.join(ctx)

            await self.MusicManager.queue_add(players=player, ctx=ctx)

            if not await self.MusicManager.play(ctx):
                await ctx.send(f"{player[0].title}??? ??????????????? ???????????????.")
            else:
                await ctx.send("???",delete_after=5)
        else:
            await ctx.send("????????? ?????? ????????????.")

    # cog error handler
    async def cog_command_error(
            self, ctx: commands.Context, error: commands.CommandError
    ):
        print("An error occurred: {}".format(str(error)))

    # Error handler
    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_music_error(self, ctx, error):
        errors = {
            discordSuperUtils.NotPlaying: "????????? ????????? ??????????????? ?????????..",
            discordSuperUtils.NotConnected: '?????? ?????? ??????????????? ??????????????? ?????????!',
            discordSuperUtils.NotPaused: "????????? ?????? ?????????????????????!",
            discordSuperUtils.QueueEmpty: "?????? ???????????????!",
            discordSuperUtils.AlreadyConnected: "?????? ??????????????? ?????????????????????!",
            discordSuperUtils.QueueError: "?????? ????????? ????????????!",
            discordSuperUtils.SkipError: "????????? ????????? ?????????!",
            discordSuperUtils.UserNotConnected: "??????????????? ?????? ??????????????? ??????????????? ?????????!",
            discordSuperUtils.InvalidSkipIndex: "????????????????????? ????????? ?????? ?????????!",
        }

        for error_type, response in errors.items():
            if isinstance(error, error_type):
                await ctx.send(response)
                return

        print("unexpected error")
        raise error

    # On music play event
    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_play(self, ctx, player):  # This returns a player object

        # Extracting useful data from player object
        thumbnail = player.data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
        title = player.data["videoDetails"]["title"]
        url = player.url
        uploader = player.data["videoDetails"]["author"]
        requester = player.requester.mention if player.requester else "Autoplay"

        embed = discord.Embed(
            title="?????? ???",
            color=discord.Color.from_rgb(255, 255, 0),
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            description=f"[**{title}**]({url}) by **{uploader}**",
        )
        embed.add_field(name="?????????", value=requester)
        embed.set_thumbnail(url=thumbnail)

        await ctx.send(embed=embed)
        # Clearing skip votes for each song
        if self.skip_votes.get(ctx.guild.id):
            self.skip_votes.pop(ctx.guild.id)

    # On queue end event
    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_queue_end(self, ctx):
        print(f"The queue has ended in {ctx}")
        await ctx.send("?????? ????????????.")
        # You could wait and check activity, etc...

    # On inactivity disconnect event
    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_inactivity_disconnect(self, ctx):
        print(f"I have left {ctx} due to inactivity")
        await ctx.send("?????????????????? ???????????? ????????????")

    # On ready event

    # Leave command
    @commands.command(name="??????")
    async def leave(self, ctx):
        if await self.MusicManager.leave(ctx):
            await ctx.send("????", delete_after=5)
            # Or
            # await message.add_reaction("????")

    # Lyrics command

    # Now playing command
    @commands.command(name="?????????", aliases = ["?????????"])
    async def now_playing(self, ctx):
        if player := await self.MusicManager.now_playing(ctx):
            # Played duration
            duration_played = round(
                await self.MusicManager.get_player_played_duration(ctx, player)
            )

            # Loop status
            loop = (await self.MusicManager.get_queue(ctx)).loop
            if loop == discordSuperUtils.Loops.LOOP:
                loop_status = "??????????????? ????????? ????????????. ????"
            elif loop == discordSuperUtils.Loops.QUEUE_LOOP:
                loop_status = "??? ??????????????? ????????? ????????????. ????"
            else:
                loop_status = "?????? ????????? ???????????? ????????????. ?????? ????"

            # Fecthing other details
            thumbnail = player.data["videoDetails"]["thumbnail"]["thumbnails"][-1][
                "url"
            ]
            title = player.data["videoDetails"]["title"]
            url = player.url
            uploader = player.data["videoDetails"]["author"]
            requester = player.requester.mention if player.requester else "Autoplay"

            embed = discord.Embed(
                title="?????????",
                description=f"**{title}**",
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.from_rgb(0, 255, 255),
            )
            embed.add_field(name="?????? ????????????", value=parse_duration(duration_played))
            embed.add_field(name="????????????", value=parse_duration(player.duration))
            embed.add_field(name="????????????", value=loop_status)
            embed.add_field(name="?????????", value=requester)
            embed.add_field(name="?????????", value=uploader)
            embed.add_field(name="URL", value=f"[Click]({url})")
            embed.set_thumbnail(url=thumbnail)
            embed.set_image(url=r"https://i.imgur.com/ufxvZ0j.gif")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    # Join voice channel command
    @commands.command(name="?????????")
    async def join(self, ctx):
        if await self.MusicManager.join(ctx):
            await ctx.send(f"{ctx.author.voice.channel.mention}??? ???????????????!")

    # Play song command
    @commands.command(name="??????")
    async def play(self, ctx, *, query: str):
        # Calling the play function
        await Music.play_cmd(self, ctx, query)

    # Pause command
    @commands.command(name="????????????")
    async def pause(self, ctx):
        if await self.MusicManager.pause(ctx):
            await ctx.send("?????????????????????. ???",delete_after=5)

    # Resume command
    @commands.command(name="????????????")
    async def resume(self, ctx):
        if await self.MusicManager.resume(ctx):
            await ctx.send("????????? ???????????????. ???", delete_after=5)

    # Volume command
    @commands.command(name="??????")
    async def volume(self, ctx, volume: int = None):
        if volume is None:
            current_volume = await self.MusicManager.volume(ctx)
            await ctx.send("?????? ?????? " + current_volume + "%")
        if await self.MusicManager.volume(ctx, volume) is not None:
            current_volume = await self.MusicManager.volume(ctx, volume)
            await ctx.send(f"????????? ???????????? ???????????????. `{current_volume}%`")

    # Song loop command
    @commands.command(name="??????", aliases = ["??????"])
    async def loop(self, ctx):
        is_loop = await self.MusicManager.loop(ctx)

        if is_loop is not None:
            await ctx.send(
                f"??????????????? {'????????? ????' if is_loop else '???????????? ????'} ?????????", delete_after=5)

    # Queue loop command
    @commands.command(name="?????????")
    async def queueloop(self, ctx):
        is_loop = await self.MusicManager.queueloop(ctx)

        if is_loop is not None:
            await ctx.send(
                f"?????????????????? {'????????? ????' if is_loop else '???????????? ????'} ?????????", delete_after=5)

    # History command
    @commands.command(name="????????????")
    async def history(self, ctx):
        if queue := await self.MusicManager.get_queue(ctx):
            auto = "Autoplay"
            formatted_history = [
                f"??????: '{x.title}\n?????????: {x.requester.mention if x.requester else auto}"
                for x in queue.history
            ]

            embeds = discordSuperUtils.generate_embeds(
                formatted_history,
                "?????? ??????",
                "???????????? ????????? ?????? ????????? ???????????????",
                25,
                string_format="{}",
            )

            for embed in embeds:
                embed.timestamp = datetime.datetime.utcnow()

            await discordSuperUtils.PageManager(ctx, embeds, public=True).run()

    # Stop command
    @commands.command(name="??????", aliases = ["??????"])
    async def stop(self, ctx):
        await self.MusicManager.cleanup(ctx.voice_client, ctx.guild)
        await ctx.send("??????")

    # Skip command with voting
    @commands.command(name="??????")
    async def skip(self, ctx, index: int = None):
        if queue := (await self.MusicManager.get_queue(ctx)):
            requester = (await self.MusicManager.now_playing(ctx)).requester

            # Checking if the song is autoplayed
            if requester is None:
                await ctx.send("???????????? ?????? ???????????????.???")
                await self.MusicManager.skip(ctx, index)

            # Checking if queue is empty and autoplay is disabled
            elif not queue.queue and not queue.autoplay:
                await ctx.send("?????? ????????? ?????? ????????? ??? ?????????")

            else:
                # Checking if guild id list is in skip votes dictionary
                if not self.skip_votes.get(ctx.guild.id):
                    self.skip_votes[ctx.guild.id] = []

                # Checking the voter
                voter = ctx.author

                # If voter is requester than skips automatically
                if voter == (await self.MusicManager.now_playing(ctx)).requester:
                    skipped_player = await self.MusicManager.skip(ctx, index)

                    await ctx.send("???????????? ???????????? ???????????????. ???",delete_after=5)

                    if not skipped_player.requester:
                        await ctx.send("?????? ????????????????????? ???????????????. ???",delete_after=5)

                    # clearing the skip votes
                    self.skip_votes.pop(ctx.guild.id)

                # Voting
                elif (
                        voter.id not in self.skip_votes[ctx.guild.id]
                ):  # Checking if someone already voted
                    # Adding the voter id to skip votes
                    self.skip_votes[ctx.guild.id].append(voter.id)

                    # Calculating total votes
                    total_votes = len(self.skip_votes[ctx.guild.id])

                    # If total votes >=3 then it will skip
                    if total_votes >= 3:
                        skipped_player = await self.MusicManager.skip(ctx, index)

                        await ctx.send("????????? ?????????????????????. ???",delete_after=5)

                        if not skipped_player.requester:
                            await ctx.send("?????? ????????????????????? ???????????????. ???",delete_after=5)

                        # Clearing skip votes of the guild
                        self.skip_votes.pop(ctx.guild.id)

                    # Shows voting status
                    else:
                        await ctx.send(
                            f"?????? ????????? ??????????????????, ?????? ????????? -  **{total_votes}/3**"
                        )

                # If someone uses vote command twice
                else:
                    await ctx.send("?????? ???????????? ??????????????????!",delete_after=5)

    # Queue command
    @commands.command(name="???",  aliases = ["????????????"])
    async def queue(self, ctx):
        if queue := await self.MusicManager.get_queue(ctx):
            auto = "Autoplay"
            formatted_queue = [
                f"??????: '{x.title}\n?????????: {x.requester.mention if x.requester else auto}"
                for x in queue.queue
            ]

            embeds = discordSuperUtils.generate_embeds(
                formatted_queue,
                "???",  # Title of embed
                f"Now Playing: {await self.MusicManager.now_playing(ctx)}",
                25,  # Number of rows in one pane
                string_format="{}",
                color=11658814,  # Color of embed in decimal color
            )

            for embed in embeds:
                embed.timestamp = datetime.datetime.utcnow()

            await discordSuperUtils.PageManager(ctx, embeds, public=True).run()

    # Loop status command
    @commands.command(name="????????????")
    async def loop_check(self, ctx):
        if queue := await self.MusicManager.get_queue(ctx):
            loop = queue.loop
            loop_status = None

            if loop == discordSuperUtils.Loops.LOOP:
                loop_status = "?????? ????????? ????????? ????????????. ????"

            elif loop == discordSuperUtils.Loops.QUEUE_LOOP:
                loop_status = "??? ?????? ????????? ????????? ????????????. ????"

            elif loop == discordSuperUtils.Loops.NO_LOOP:
                loop_status = "?????? ????????? ???????????? ????????????. ????"

            if loop_status:
                embed = discord.Embed(
                    title=loop_status,
                    color=0x00FF00,
                    timestamp=datetime.datetime.utcnow(),
                )

                await ctx.send(embed=embed)

    # Shuffle command
    @commands.command(name="??????")
    async def shuffle(self, ctx):
        is_shuffle = await self.MusicManager.shuffle(ctx)

        if is_shuffle is not None:
            if is_shuffle:
                await ctx.send('????????? ?????????????????????.',delete_after=5)
            else:
                await ctx.send('????????? ????????????????????????.',delete_after=5)

    # Previous/Rewind command
    @commands.command(name="?????????")
    async def previous(self, ctx, index: int = None):
        if previous_player := await self.MusicManager.previous(ctx, index):
            await ctx.send(f"{previous_player[0].title}????????? ???????????? ????????????",delete_after=5)

    # Before invoke checks. Add more commands if you wish to
    @join.before_invoke
    @play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("You are not connected to any voice channel.")
            raise commands.CommandError()

        if (
                ctx.voice_client
                and ctx.voice_client.channel != ctx.author.voice.channel
        ):
            await ctx.send("Bot is already in a voice channel.")
            raise commands.CommandError()


def setup(bot):
    bot.add_cog(Music(bot))