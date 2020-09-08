import asyncio
import discord
from discord.ext import commands
import random
from discord.utils import get
import os
import shutil
import json
import time

class manage(commands.Cog, name='관리'): #2

    def __init__(self, bot): #3
        self.bot = bot #4
    
    @commands.command(name="추방", pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, *, user_name: discord.Member, reason=None):
        await user_name.kick(reason=reason)
        await ctx.send(str(user_name)+"을(를) 추방하였습니다.")
    @_kick.error
    async def _kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("유저를 넣어주세요.")
    
    @commands.command(name="밴", pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, *, user_name: discord.Member):
        await user_name.ban()
        await ctx.send(str(user_name)+"을(를) 영원히 매장시켰습니다.")
    @_ban.error
    async def _ban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("유저를 넣어주세요.")
            
    @commands.command(name="언밴", pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def _unban(self, ctx, *, user_name):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = user_name.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention}을(를) 죽였었으나 다시 살리고있습니다.")
                return
    @_unban.error
    async def _unban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("유저를 넣어주세요.")


    @commands.command(name="청소", pass_context=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def _clear(self, ctx, *, amount:int):
        if amount <= 100:
            await ctx.channel.purge(limit=amount+1)
        elif amount >= 101:
            await ctx.send("숫자가 너무 커요! 100이하로 해주세요!")
        elif amount <= 0:
            await ctx.send("숫자가 너무 작요! 1이상으로 해주세요!")
    @_clear.error
    async def _clear_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("**수**를 넣어주세요.")
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')
 

    @commands.command(name="경고")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        guild_id = str(ctx.message.guild.id)
        if reason is None:
            reason = '없음'

        data_exist = os.path.isfile(f"data/guild_data/{guild_id}/admin.json")
        if data_exist:
            pass
        else:
            try:
                shutil.copy('data/guild_data/data.json', f'data/guild_data/{guild_id}/admin.json')
            except:
                os.mkdir(f'data/guild_data/{guild_id}/')
                shutil.copy('data/guild_data/data.json', f'data/guild_data/{guild_id}/admin.json')

        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        try:
            warn_data[str(member.id)]["warn"][str(time.strftime('%Y%m%d%H%M%S'))] = f"{reason}, by {ctx.author}"
        except KeyError:
            warn_data[str(member.id)] = {}
            warn_data[str(member.id)]["warn"] = {}
            warn_data[str(member.id)]["warn"][str(time.strftime('%Y%m%d%H%M%S'))] = f"{reason}, by <@{ctx.author.id}>"

        with open(f'data/guild_data/{guild_id}/admin.json', 'w') as s:
            json.dump(warn_data, s, indent=4)

        await ctx.send(f"{member.mention}님에게 경고가 주어졌습니다. (이유: {reason}, 번호: {str(time.strftime('%Y%m%d%H%M%S'))})")
    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("**수**를 넣어주세요.")

    @commands.command(name="누적경고", aliases= ['경고확인'])
    async def warncheck(self, ctx, member: discord.Member = None):
        guild_id = str(ctx.message.guild.id)
        member = ctx.author if not member else member

        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        global cases

        try:
            cases = str(warn_data[str(member.id)]["warn"].keys())
        except KeyError:
            cases = None

        if cases is None:
            cases = '아무 경고도 존재하지 않습니다.'

        else:
            cases = cases.lstrip('dict_keys([')
            cases = cases.rstrip('])')

        embed = discord.Embed(title='누적된 경고', description=f'유저: {member}', colour=discord.Color.red())
        embed.add_field(name='경고 번호', value=f'{cases}')

        await ctx.send(embed=embed)

    @warncheck.error
    async def warncheck_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("**수**를 넣어주세요.")

    @commands.command(name="경고정보")
    async def warninfo(self, ctx, member: discord.Member, num):
        global case
        guild_id = str(ctx.message.guild.id)
        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        try:
            case = warn_data[str(member.id)]["warn"][str(num)]
        except KeyError:
            await ctx.send('정보가 존재하지 않습니다.')
            return

        # embed 탬플릿 (앞에 #을 지우고 사용하세요)
        # embed.add_field(name='', value='')
        # embed.add_field(name='', value='', inline=False)

        embed = discord.Embed(title='경고 세부 정보', description=f'유저: {member}', colour=discord.Color.red())
        embed.add_field(name='경고 번호', value=f'{num}')
        embed.add_field(name='경고 이유 및 경고 발급 유저', value=f'{case}', inline=False)

        await ctx.send(embed=embed)
    @warninfo.error
    async def warninfo_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("**수**를 넣어주세요.")

    @commands.command(name="경고삭제")
    @commands.has_permissions(kick_members=True)
    async def warndelete(self, ctx, member: discord.Member, num):
        guild_id = str(ctx.message.guild.id)

        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        try:
            del warn_data[str(member.id)]["warn"][str(num)]

        except KeyError:
            await ctx.send('존재하지 않는 경고입니다.')
            return

        with open(f'data/guild_data/{guild_id}/admin.json', 'w') as s:
            json.dump(warn_data, s, indent=4)

        await ctx.send('경고가 삭제되었습니다.')
    @warndelete.error
    async def warndelete_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("**수**를 넣어주세요.")

    @commands.command(name="슬로우모드", aliases=['슬로우'])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, num: int, chan: discord.TextChannel = None):
        if chan is None:
            chan = ctx.message.channel
        if num < 0:
            await ctx.send("0보다 큰 수로 입력해주세요.")
            return

        await chan.edit(slowmode_delay=num)
        if num == 0:
            await ctx.send("슬로우모드를 껐어요!")
            return
        await ctx.send(f"{chan.mention}에 {num}초 슬로우모드를 걸었어요!")
    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("**수**를 넣어주세요.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def 역할추가(self, ctx, member: discord.Member, *, role):
        role = discord.utils.get(ctx.guild.roles, name=str(role))
        await member.add_roles(role)
        await ctx.send(f'{member.mention}님에게 `{role.name}` 역할을 추가했습니다.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def 역할제거(self, ctx, member: discord.Member, *, role):
        role = discord.utils.get(ctx.guild.roles, name=str(role))
        await member.remove_roles(role)
        await ctx.send(f'{member.mention}님의 `{role.name}` 역할을 제거했습니다.')

def setup(bot): #5
    bot.add_cog(manage(bot))