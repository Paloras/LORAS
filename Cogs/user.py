
import discord
from discord.ext import commands
import datetime

class Userinfo(commands.Cog, name='정보'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="유저", help="유저정보를 알려줍니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def userinfo(self, ctx):
        if (ctx.message.mentions.__len__() > 0):
            for user in ctx.message.mentions:
                status_dict: dict = {discord.Status.online: '<:online:708147696879272027> 온라인', discord.Status.offline: '<:offline:708147696523018255> 오프라인', discord.Status.idle: "<:idle:708147696807968842> 자리비움", discord.Status.do_not_disturb: "<:dnd:708147696976003092> 방해금지"}
                user_status = status_dict[user.status]
                roles_list = [r.mention.replace(f'<@&{ctx.guild.id}>', '@everyone') for r in reversed(sorted(user.roles, key=lambda role: role.position))]
                roles = ', '.join(roles_list)
                embed = discord.Embed(title="**" + user.name+ "#" +user.discriminator + "**님의 정보", description="",colour=discord.Color.red())
                embed.add_field(name="**ID**", value=user.id, inline=True)
                embed.add_field(name="**이름**", value=user.name, inline=True)
                embed.add_field(name="**닉네임**", value=user.display_name, inline=True)
                embed.add_field(name="**상태**", value=user_status, inline=True)
                embed.add_field(name='**계정이 생성된 날짜**', value=user.created_at.strftime("%Y-%m-%d %I:%M:%S %p"))
                embed.add_field(name='**서버에 들어온 날짜**', value=user.joined_at.strftime("%Y-%m-%d %I:%M:%S %p"), inline=False)
                embed.add_field(name='**역할**', value=user.top_role.mention)
                embed.add_field(name='**모든역할**', value=roles)
                embed.add_field(name="**언급**", value="<@" + str(user.id) + ">", inline=True)
                embed.set_thumbnail(url=user.avatar_url)
                await ctx.send(embed=embed)
        else:
            roles_list = [r.mention.replace(f'<@&{ctx.guild.id}>', '@everyone') for r in reversed(sorted(ctx.author.roles, key=lambda role: role.position))]
            roles = ', '.join(roles_list)
            status_dict: dict = {discord.Status.online: '<:online:708147696879272027> 온라인', discord.Status.offline: '<:offline:708147696523018255> 오프라인', discord.Status.idle: "<:idle:708147696807968842> 자리비움", discord.Status.do_not_disturb: "<:dnd:708147696976003092> 방해금지"}
            user_status = status_dict[ctx.author.status]
            embed = discord.Embed(title=ctx.author.name+ "#" +ctx.author.discriminator + "님의 정보", description="", colour=discord.Color.red())
            embed.add_field(name="**ID**", value=ctx.author.id, inline=True)
            embed.add_field(name="**닉네임**", value=ctx.author.display_name, inline=True)
            embed.add_field(name="**상태**", value=user_status, inline=True)
            embed.add_field(name='**계정이 생성된 날짜**', value=ctx.author.created_at.strftime("%Y-%m-%d %I:%M:%S %p"))
            embed.add_field(name='**서버에 들어온 날짜**', value=ctx.author.joined_at.strftime("%Y-%m-%d %I:%M:%S %p"), inline=False)
            embed.add_field(name='**가지고 있는 최고역할**', value=ctx.author.top_role.mention)
            embed.add_field(name='**모든역할**', value=roles)
            embed.add_field(name="**언급**", value="<@" + str(ctx.author.id) + ">", inline=True)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="프사",aliases=['아바타'], help="남의 프사를 가져옵니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def avatar(self, ctx):
        if (ctx.message.mentions.__len__() > 0):
            for user in ctx.message.mentions:
                pfp = str(user.avatar_url)
                embed = discord.Embed(title="**" +user.name + "**님의 아바타", description="[Link]" + "(" + pfp + ")", color=0xffffff)
                embed.set_image(url=pfp)
                await ctx.trigger_typing()
                await ctx.send(embed=embed)
        else:
            pfp = ctx.author.avatar_url
            embed = discord.Embed(title="**" + ctx.author.name + "**님의 아바타", description="[Link]" + "(" + str(pfp) + ")", color=0xffffff)
            embed.set_image(url=pfp)
            await ctx.trigger_typing()
            await ctx.send(embed=embed)
    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="서버", aliases=['서버정보'], help="서버정보를 알아냅니다")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def serverinfo(self, ctx):
        roles = ctx.guild.roles
        embed = discord.Embed(title='서버정보', colour=discord.Color.red())
        embed.set_author(name=f'{ctx.guild.name}', icon_url=ctx.guild.icon_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name='소유자', value=f'{ctx.guild.owner} /id:{ctx.guild.owner.id}', inline=False)
        embed.add_field(name='유저수', value=f'{len(list(filter(lambda x: not x.bot, ctx.guild.members)))}명', inline=False)
        embed.add_field(name='봇수', value=f'{len(list(filter(lambda x: x.bot, ctx.guild.members)))}개', inline=False)
        embed.add_field(name='서버가 생성된 날짜', value=f'{ctx.guild.created_at.strftime("%Y-%m-%d %I:%M:%S %p")}',
                        inline=False)
        embed.add_field(name="채널수", value=f"채팅 채널 {str(len(ctx.guild.text_channels))}개\n음성 채널 {str(len(ctx.guild.voice_channels))}개\n카테고리 {str(len(ctx.guild.categories))}개", inline=False)
        embed.add_field(name='역할수', value=str(len(ctx.guild.roles)) + '개', inline=False)
        embed.add_field(name="서버 이모지 수", value = f'{len(ctx.guild.emojis)}개', inline=False)
        embed.add_field(name="서버 부스트 레벨", value=str(ctx.guild.premium_tier) + '레벨', inline=False)
        embed.add_field(name="서버 부스트 수", value=str(ctx.guild.premium_subscription_count) + '개', inline=False)
        embed.add_field(name='서버 최고 역할', value=f'{roles[-1].mention}', inline=False)
        embed.add_field(name='서버 위치', value=f'{ctx.guild.region}', inline=False)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="서버역할", aliases=['역할'], help="서버에 있는 역할을 알려줍니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def serverroleinfo(self, ctx):
        roles_list = [r.mention.replace(f'<@&{ctx.guild.id}>', '@everyone') for r in reversed(sorted(ctx.guild.roles, key=lambda role: role.position))]
        roles = ', '.join(roles_list)
        if len(roles)> 2048:
            embed = discord.Embed(title='서버역할', description = roles[:2038], colour=discord.Color.red())
            embed.add_field(name='ㅤ', value=roles[2039:], inline=False)
            embed.set_author(name=f'{ctx.guild.name}', icon_url=ctx.guild.icon_url)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name='역할수', value=str(len(ctx.guild.roles)) + '개', inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        if len(roles)<= 2048:
            embed = discord.Embed(title='서버역할', description = roles, colour=discord.Color.red())
            embed.set_author(name=f'{ctx.guild.name}', icon_url=ctx.guild.icon_url)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name='역할수', value=str(len(ctx.guild.roles)) + '개', inline=False)
            embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    @serverroleinfo.error
    async def serverroleinfo_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="서버이모티콘", aliases=['서버이모지', '이모지'], help="서버에 있는 커스텀 이모지들을 알려줍니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def serveremoji(self, ctx):
        if ctx.guild.emojis:
            emotes = ''.join((str(x) for x in ctx.guild.emojis))
        embed = discord.Embed(title=f'서버이모지({len(ctx.guild.emojis)}개)', description = emotes, colour=discord.Color.red())
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @serveremoji.error
    async def serveremoji_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')


    @commands.command(name="서버채널", aliases=['채널'],help="서버에 있는 채널들을 알려줍니다.")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def serverchannel(self, ctx):
        if ctx.guild.text_channels:
            text = ','.join((str(x.mention) for x in ctx.guild.text_channels))
        if ctx.guild.voice_channels:
            voice1 = (str(x.mention) for x in ctx.guild.voice_channels)
            voice = ','.join((str(x.mention) for x in ctx.guild.voice_channels))
        embed = discord.Embed(title='음성 채널', description=voice, colour=discord.Color.red())
        embed.set_author(name=f'{ctx.guild.name}', icon_url=ctx.guild.icon_url)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)

        embed1 = discord.Embed(title='채팅 채널', description=text, colour=discord.Color.red())
        embed.set_author(name=f'{ctx.guild.name}', icon_url=ctx.guild.icon_url)
        embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
        await ctx.send(embed=embed1)
    @serverchannel.error
    async def serverchannel_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    
    @commands.command(name="봇정보", aliases=['크레딧'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def botinfooo(self, ctx):
        embed = discord.Embed(title=f"{self.bot.user.name}", colour=discord.Colour.green())
        embed.add_field(name="개발자", value=self.bot.get_user(384227121267998722), inline=False)
        embed.add_field(name="만들어진 날짜", value="2020-06-19 01:20:31 AM", inline=False)
        embed.add_field(name="사용하는 서버 수 / 유저", value=f"{len(self.bot.guilds)}개의 서버 / {len(self.bot.users)}명의 유저", inline=False)
        embed.add_field(name="참고및 쓰고 있는 오픈소스 : ", value="[링크1](https://github.com/Team-EG/j-bot-old)|제작자: eunwoo1104님-게임,경고 \n[링크2](https://github.com/J-hoplin1/League-Of-Legend-Search-Bot)|제작자: J-hoplin1님-롤 \n[링크3](https://github.com/J-hoplin1/PUBG-player-search-bot/blob/6676975cef8d70da5ffc6fac657f9f5911f0b654/PUBGSearchbot.py)|제작자: J-hoplin1님-배그", inline=False)
        embed.set_footer(text=ctx.author.name + str(datetime.datetime.utcnow()), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @botinfooo.error
    async def botinfooo_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

def setup(bot):
    bot.add_cog(Userinfo(bot))
