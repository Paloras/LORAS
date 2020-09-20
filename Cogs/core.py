# To make a discord bot you need to download discord.py with pip
#-*- coding: utf-8 -*-
import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import datetime
from captcha.image import ImageCaptcha
import time
import ast
import json
from config import OWNERS

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class Core(commands.Cog, name='부가기능'): #2

    def __init__(self, bot): #3
        self.bot = bot #4

    @commands.command(name="따라해", aliases=['따라하기'], help="따라합니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def repeat(self, ctx, *, content):
        await ctx.send(f"{content}")
    @repeat.error
    async def repeat_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="핑", help="봇의 핑을 알려줍니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ping(self, ctx):
        embed=discord.Embed(title="퐁!", description=str(round(self.bot.latency * 1000)) + "ms", color=0xff752e)
        await ctx.send(embed=embed)
    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')
    
    @commands.command(name="건의")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def dsdsadadafasf(self,ctx, *, massage):
        cha = self.bot.get_channel(111111111111111111)
        embed = discord.Embed(title=f"{ctx.author.name} // {ctx.author.id}", description= "건의내용\n"+massage,colour=discord.Colour.green())
        embed.set_footer(text=f"{ctx.author} 시간: "+str(datetime.datetime.utcnow()), icon_url=ctx.author.avatar_url)
        await cha.send(embed=embed)
        await ctx.send("성공적으로 보내졌습니다.")
    @dsdsadadafasf.error
    async def dsdsadadafasf_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="문의")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def sddsds(self,ctx, *, massage):
        cha = self.bot.get_channel(111111111111111111)
        embed = discord.Embed(title=f"{ctx.author.name} // {ctx.author.id}", description= "문의내용\n"+massage,colour=discord.Colour.green())
        embed.set_footer(text=f"{ctx.author} 시간: "+str(datetime.datetime.utcnow()), icon_url=ctx.author.avatar_url)
        await cha.send(embed=embed)
        await ctx.send("성공적으로 보내졌습니다.")
    @sddsds.error
    async def sddsds_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="답변")
    async def adasdasdafasfcsad(self, ctx, user:int, *, response):
        if ctx.author.id == 111111111111111111:
            idds = self.bot.get_user(user)
            embed = discord.Embed(title=f"답변 내용", description= response, colour=discord.Colour.green())
            embed.set_footer(text=f"{ctx.author} 시간: "+str(datetime.datetime.utcnow()), icon_url=ctx.author.avatar_url)
            await idds.send(embed=embed)
            await ctx.send("성공적으로 보내졌습니다.")
        else:
            await ctx.send("이 명령어를 쓰려면 최소 Bot Developer 권한이 필요합니다.")
    @adasdasdafasfcsad.error
    async def adasdasdafasfcsad_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="시간", aliases=['타임', '현재시간'], help="현재시간을 알려줍니다")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def time(self,ctx):
        await ctx.send(embed=discord.Embed(title="Time", timestamp=ctx.message.created_at))
    @time.error
    async def time_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')
    
    @commands.command(name="투표", help="투표를 엽니다")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def vote(self,ctx,*, content):
        emo = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
        vote = content.split("/")
        if len(vote)> 11:
            await ctx.send("너무 길어요")
        elif len(vote)<= 11 and len(vote)>= 3:
            T =""
            Tt = "⭐투표 - **" + vote[0] + "**"
            for i in range(1, len(vote)):
                T += f"{i}. \n**" + vote[i] + "**\n\n"
            embed = discord.Embed(title=Tt, description=T, color=ctx.author.color)
            co = await ctx.send(embed=embed)
            for i in range(len(vote)-1):
                await co.add_reaction(emo[i])
        elif len(vote)< 3:
            await ctx.send("너무 짧아요")
            return

    @vote.error
    async def vote_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name = 'eval', aliases=['이발'])
    async def eval_fn(self, ctx, *, cmd):
        if ctx.author.id == 111111111111111111:
            try:
                fn_name = "_eval_expr"
                cmd = cmd.strip("` ")
                cmd = "\n".join(f"{i}" for i in cmd.splitlines())
                body = f"async def {fn_name}():\n{cmd}"
                parsed = ast.parse(body)
                body = parsed.body[0].body
                insert_returns(body)
                env = {
                    'bot': self.bot,
                    'discord': discord,
                    'commands': commands,
                    'ctx': ctx,
                    '__import__': __import__
                    }
                exec(compile(parsed, filename="<ast>", mode="exec"), env)

                result = (await eval(f"{fn_name}()", env))

                embed = discord.Embed(title="EVAL 실행 결과", description=f"**Input**\n```{cmd} ```\n**Output**\n```{result}```", color=0x00ff00)
                await ctx.send(embed=embed)
                # await ctx.send(result)
            except Exception as e:
                embed = discord.Embed(title="EVAL 실행 결과", description=f"**Input**\n```{cmd} ```\n**Output**\n```{e}```", color=0xff0000)
                await ctx.send(embed=embed)
        else:
            await ctx.send("봇개발자만 가능합니다.")
    
    @commands.command(name="샤드")
    @commands.guild_only()
    async def guild_shard(self, ctx):
        embed = discord.Embed(
            title="샤드",
            description="현재 이 서버는 샤드 {}번에 있어요!".format(ctx.guild.shard_id),
            color=0x237CCD,
        )
        await ctx.send(embed=embed)
    
    @commands.command(name="공지설정")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setannouncechannel(self, ctx):
        guild_id = str(ctx.guild.id)
        with open(f'game/data.json', 'r') as f:
            channel = json.load(f)
        channel[guild_id] = {}
        channel[guild_id]['announce'] = str(ctx.channel.id)
        with open(f'game/data.json', 'w') as s:
            json.dump(channel, s, indent=4)
        await ctx.send(f'해당 채널({ctx.channel.mention})이 공지 설정이 되었습니다.')
    
    @commands.command(name="공지")
    @commands.guild_only()
    async def announce(self, ctx, *, msg):
        a=0
        if ctx.author.id in OWNERS:
            embed = discord.Embed(  title = "로라스 공지",description = msg + f"\n\n이 채널에 공지가 오기 싫다면 공지설정을 해주세요!\n[서포트 서버](https://discord.gg/SVDm3hg)",colour = 0xffffff,timestamp = ctx.message.created_at)
            embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'{ctx.message.author}')
            embed.set_thumbnail(url=self.bot.user.avatar_url_as(format=None, static_format="png", size=1024))
            with open(f'game/data.json', 'r') as f:
                channel = json.load(f)
            for i in channel:
                cha = self.bot.get_channel(int(channel[i]['announce']))
                await cha.send(embed=embed)
                a+=1
            await ctx.send(f"{a}개의서버에 전송완료")
        else:
            await ctx.send("개발자가 아닙니다.")

def setup(bot): #5
    bot.add_cog(Core(bot))
