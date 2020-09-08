import discord
from discord.ext import commands
import ast
import asyncio
import math
import wolframalpha

class calculate(commands.Cog, name='계산'):

    def __init__(self, bot):
        self.bot = bot



    @commands.command(name="최대공약수", help="최대공약수를 구해줘여!\n사용법 : 팔최대공약수 (숫자1) (숫자2)")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gcd2(self, ctx, x:int, y:int):
        def gcd2(x,y):
            if y == 0:
                return x
            else:
                if (x < y):
                    x,y =y,x
                return gcd2(y, x%y)
        await ctx.send(f'결과 : {gcd2(y,x)}')
    @gcd2.error
    async def gcd2_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="최소공배수", help="최소공배수를 구해줘여!\n사용법 : 팔최소공배수 (숫자1) (숫자2)")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gcd(self, ctx, x:int, y:int):
        def gcd(x,y):
            if y == 0:
                return x
            else:
                if x < y:
                    x,y =y,x
                return gcd(y, x%y)
        def len(x,y):
            return x * y // gcd(x,y)
        await ctx.send(f'결과 : {len(y,x)}')
    @gcd.error
    async def gcd_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')
    
    @commands.command(name="제곱근", help='제곱근을 구해줍니다.\n사용법 팔제곱근 (숫자)')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def sqrt(self, ctx, *, amount:int):
        await ctx.send(math.sqrt(amount))
    @sqrt.error
    async def sqrt_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="근", help='근을 구해줍니다.\n사용법 팔근 (숫자)')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def d(self, ctx, x:float, y:float, z:float):
        if x == 0:
            await ctx.send("이차방정식이 아니예요")
        D = y*y-4*x*z
        M = y/-2*x
        if D > 0:
            x1 = (-y+math.sqrt(D))/(2*x)
            x2 = (-y-math.sqrt(D))/(2*x)
            await ctx.send(f"두개의 해: {x1}, {x2} | 대칭축: {M}")
        if D == 0:
            x1 = -y/(2*x)
            await ctx.send(f"한개의 해: {x1} | 대칭축: {M}")
        if D < 0:
            await ctx.send(f"해가 없음 | 대칭축: {M}")
    @d.error
    async def d_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("팔근 a b c (`ax²+bx+c`에서 x²의 계수인 a와 x의 계수 b 그리고 상수c를 넣어주세요)")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("**수**를 넣어주세요.")
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="진법", help='근을 구해줍니다.\n사용법 팔진법 (진법) (변환할 수)')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def gadadd(self, ctx, 진법:int, 변환할수):
        if 진법 == 2:
            await ctx.send(bin(변환할수))
        elif 진법 == 8:
            await ctx.send(oct(변환할수))
        elif 진법 == 16:
            await ctx.send(hex(변환할수))
        elif 진법 == 10:
            await ctx.send(int(변환할수))
        elif 진법 != 2 or 진법 != 8 or 진법 != 10 or 진법 != 16:
            await ctx.send("지원하지 않는 진수입니다.")

        # def make_base(n, base):
        #     v_list = ['0','1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D']
        #     q = n // base
        #     r = n % base
        #     rr = v_list[r]
    
        #     if q == 0:
        #         return rr
        #     else:
        #         return make_base(q, base) + rr
        # await ctx.send(f"결과: {make_base(y, x)}")

    @gadadd.error
    async def gadadd_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("**수**를 넣어주세요.")
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

    @commands.command(name="계산기", aliases=['계산'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def calcula(self, ctx, *, 식):
        app_id="app_id"
        wolfi=wolframalpha.Client(app_id)
        res = wolfi.query(식)
        await ctx.send(next(res.results).text)
    @calcula.error
    async def calcula_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.message.add_reaction('<:2s:752150489348571197>')

def setup(bot):
    bot.add_cog(calculate(bot))
