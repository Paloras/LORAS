#auto loop
import dbkrpy
import discord
from discord.ext import commands
import aiohttp

async def req (url : str, header = None) :
   async with aiohttp.ClientSession () as session:
      async with session.get (url = url, headers=header) as r :
         data = await r.json()
   return data

class UpdateGuild(commands.Cog, name='하트'):

    def __init__(self, bot):
        self.bot = bot
        self.token = 'dbkrtoken'
        dbkrpy.UpdateGuilds(bot,self.token)

    @commands.command(name = '확인', aliases = ['하트'])
    async def 확인(self, ctx, user:discord.User = None):
        if user == None:
            user = ctx.author
        data = await req(url= f"https://api.koreanbots.cf/bots/voted/{user.id}", header={"token":self.token,"content-type":"application/json"})
        vote = await req("https://api.koreanbots.cf/bots/get/723346442932191302")
        if data['code'] == 200:
            if data["voted"] == True:
                await ctx.send(embed = discord.Embed(title="하트확인", description = f'{user}님은 하트를 누른거같아요!!! [투표하기](https://koreanbots.cf/bots/723346442932191302) ❤️{vote["data"]["votes"]}'))
            else:
                await ctx.send(embed = discord.Embed(title="하트확인", description = f'{user}님은 하트를 안 누르신거같은데요...? [투표하기](https://koreanbots.cf/bots/723346442932191302) ❤️{vote["data"]["votes"]}'))
        else:
            await ctx.send(embed = discord.Embed(title="하트확인", description = f'{user}님은 하트를 안 누르신거같은데요...? [투표하기](https://koreanbots.cf/bots/723346442932191302) ❤️{vote["data"]["votes"]}'))
    
    @commands.command()
    async def 순위(self, ctx):
        data = await req(f'https://api.koreanbots.cf/bots/get')
        a = str()
        n = 1
        for i in data['data']:
            a += f"{n}위 - {i['name']} : {i['servers']}서버 ❤️ {i['votes']}\n"
            n += 1
        embed = discord.Embed(title="봇하트순위", description = a + f'\n[투표하기](https://koreanbots.cf/bots/723346442932191302)')
        await ctx.send(embed= embed)

def setup(bot):
    bot.add_cog(UpdateGuild(bot))
