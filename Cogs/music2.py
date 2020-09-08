# To make a discord bot you need to download discord.py with pip
#-*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord.utils import get
import urllib
from youtube_dl import YoutubeDL
from asyncio import run_coroutine_threadsafe

class Music(commands.Cog, name='음악'):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.message = {}

    @staticmethod
    def parse_duration(duration):
        result = []
        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)
        return f'{h:d}:{m:02d}:{s:02d}'

    @staticmethod
    def search(author, arg):
        with YoutubeDL(Music.YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]

            embed = (discord.Embed(title='🎵 현재 재생중인 음악 🎵 :', description=f"[{info['title']}]({info['webpage_url']})", color=discord.Color.blue())
                    .add_field(name='재생시간', value=Music.parse_duration(info['duration']))
                    .add_field(name='요청자', value=author)
                    .add_field(name='업로더', value=f"[{info['uploader']}]({info['channel_url']})")
                    .add_field(name="재생목록", value=f"재생할 다음노래가 없어요!!")
                    .set_thumbnail(url=info['thumbnail']))
            
            return {'embed': embed, 'source': info['formats'][0]['url'], 'title': info['title']}

    async def edit_message(self, ctx):
        embed = self.song_queue[ctx.guild][0]['embed']
        content = "\n".join([f"({self.song_queue[ctx.guild].index(i)}) {i['title']}" for i in self.song_queue[ctx.guild][1:]]) if len(self.song_queue[ctx.guild]) > 1 else "재생목록이 비어있어요!"
        embed.set_field_at(index=3, name="재생목록 :", value=content, inline=False)
        await self.message[ctx.guild].edit(embed=embed)

    def play_next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if len(self.song_queue[ctx.guild]) > 1:
            del self.song_queue[ctx.guild][0]
            run_coroutine_threadsafe(self.edit_message(ctx), self.bot.loop)
            voice.play(discord.FFmpegPCMAudio(self.song_queue[ctx.guild][0]['source'], **Music.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
            voice.is_playing()
        else:
            run_coroutine_threadsafe(voice.disconnect(), self.bot.loop)
            run_coroutine_threadsafe(self.message[ctx.guild].delete(), self.bot.loop)

    @commands.command(name="재생",aliases=['틀어'], brief='팔재생 [url/words]')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def 재생(self, ctx, *, arg):
        try: channel = ctx.author.voice.channel
        except: await ctx.send("❌ 당신은 아무채널에도 연결되어있지 않습니다만?", delete_after = 5.0)
        else: 
            channel = ctx.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            song = Music.search(ctx.author.mention, arg)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()     

            if not voice.is_playing():
                self.song_queue[ctx.guild] = [song]
                self.message[ctx.guild] = await ctx.send(embed=song['embed'])
                voice.play(discord.FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
                voice.is_playing()
            else:
                self.song_queue[ctx.guild].append(song)
                await self.edit_message(ctx)
    @재생.error
    async def 재생_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(brief='정지')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def 정지(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if voice.is_playing():
                await ctx.send('⏸️ 노래가 정지되었습니다.', delete_after = 5.0)
                voice.pause()
            else:
                await ctx.send('⏯️ 노래를 다시 재생합니다.', delete_after = 5.0)
                voice.resume()
        else:
            await ctx.send("❌아무 채널에도 열결되어있지 않습니다.", delete_after = 5.0)
    @정지.error
    async def 정지_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(aliases=['넘어'], brief='팔스킵')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def 스킵(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        if voice and voice.is_playing():
            await ctx.send('⏭️ 노래가 스킵됬습니다.', delete_after = 5.0)
            voice.stop()
        else:
            await ctx.send("❌ 재생할 노래가 없어요!", delete_after = 5.0)
    @스킵.error
    async def 스킵_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(brief='멈춰 [video]')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def 제거(self, ctx, *, arg):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            for video in self.song_queue[ctx.guild][1:]:
                if arg.lower() in video['title'].lower():
                    self.song_queue[ctx.guild].remove(video)
            await self.display_message(ctx)
        else:
            await ctx.send("❌ 노래를 재생하고 있지않아요!")
    @제거.error
    async def 제거_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

def setup(bot):
    bot.add_cog(Music(bot))