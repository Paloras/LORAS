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

    @commands.command(aliases=['프린트', '출력'], help="정상적동하는지 알려줍니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def printf(self, ctx):
        await ctx.channel.send("로라스에 의해 출력됨.")
    @printf.error
    async def printf_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

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
        cha = self.bot.get_channel(744449976746246206)
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
        cha = self.bot.get_channel(744449976746246206)
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
        if ctx.author.id == 384227121267998722:
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
        vote = content.split("/")
        if len(vote)> 5:
            await ctx.send("너무 길어요")
        elif len(vote)<= 5:
            await ctx.send("⭐투표 - **" + vote[0] + "**")
            for i in range(1, len(vote)):
                choose = await ctx.send("**" + vote[i] + "**")
                await choose.add_reaction('👍')
    @vote.error
    async def vote_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name = 'eval', aliases=['이발'])
    async def eval_fn(self, ctx, *, cmd):
        if ctx.author.id == 384227121267998722:
            try:
                fn_name = "_eval_expr"
                cmd = cmd.strip("` ")
                cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
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



def setup(bot): #5
    bot.add_cog(Core(bot))