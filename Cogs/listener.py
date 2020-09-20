# To make a discord bot you need to download discord.py with pip
#-*- coding: utf-8 -*-

from discord.utils import get
import discord
from discord.ext import commands
import random
import asyncio
import re
import ast
from config import OWNERS


class Events(commands.Cog):
    
    def __init__(self, bot):
        """Initialisation bot"""
        self.bot = bot
    
    def is_owner(self, ctx):
        return ctx.message.author.id in OWNERS

    @commands.Cog.listener()
    async def on_ready(self):
        print("다음으로 로그인합니다 : ")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("==========")
        print(f"New log in as {self.bot.user}")
        while True:
            user = len(self.bot.users)
            server = len(self.bot.guilds)
            mes = ["팔도움을 요구", "건의는 !  PLRS#3588에게 해주세요!", str(user) + "명의 유저들과 함께 ", str(server) + "개의 서버에 참가"]
            for m in range(len(mes)):
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=mes[m]))
                await asyncio.sleep(3)

    @commands.Cog.listener()
    async def on_message(self, message):    
        if message.author.bot:
            return None
        
        if "죽음" in message.content or "사망" in message.content or "운명" in message.content:
            await message.add_reaction('❎')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        cha = self.bot.get_channel(111111111111111111)  
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction('🚫')
            await ctx.send (f"당신이 필요한 권한을 가지고 있지 않습니다.\n필요한 권한: `{', '.join(error.missing_perms)}`", delete_after=7.0)
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('⏱️')
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author), delete_after=7.0)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"누락된 필수 항목이 있습니다. **{error.param.name}** 이것을 안 넣으신거같군요.", delete_after=7.0)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction('🤔')
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"잘못된 필수 항목이 있습니다. **{error}**", delete_after=69.0)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"잘못된 필수 항목이 있습니다. **{error}**", delete_after=69.0)
        # elif isinstance(error, commands.CheckFailure):
        #     await ctx.message.add_reaction('⛔')
        #     await ctx.send(f'[ {ctx.message.content} ] 명령을 실행하기에 권한이 부족해요')
        else:
            embed = discord.Embed(title="오류!!", description=f"```{error}```", color=0xFF0000, timestamp=ctx.message.created_at)
            embed1 = discord.Embed(title="오류!!", description="오류가 발생했습니다.", color=0xFF0000, timestamp=ctx.message.created_at)
            embed1.add_field(name="상세", value=f"사용자 : {ctx.author}\n오류난 명령어 : {ctx.message.content}\n```{error}```")
            # embed.set_footer(text=f"{ctx.author}시간 : {str(ctx.message.created_at())}", icon_url=ctx.author.avatar_url)
            await cha.send(embed=embed1)
            await ctx.send(embed=embed)
                            
def setup(bot):
    bot.add_cog(Events(bot))    
