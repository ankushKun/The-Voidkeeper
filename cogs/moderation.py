import discord
from discord.ext import commands

GODS = [272285219942301696,728044189417209856,666578281142812673]

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def announce(self,ctx,*,msg):
        if ctx.message.author.guild_permissions.administrator or ctx.author.id in GODS:
            m = ctx.guild.members
            for u in m:
                print(u)
                try:
                    if not u.bot:
                        await u.send(msg)
                except:
                    await ctx.send("could not to send to {}".format(u.mention))
        else :
            await ctx.send(f"{u.mention} you dont have admin perms")

    @commands.command(aliases=['clear','purge'])
    async def cls(self,ctx,l):
        if ctx.message.author.guild_permissions.manage_messages  or ctx.author.id in GODS:
            try:
                await ctx.channel.purge(limit=int(l)+1)
            except:
                await ctx.send("```n.cls <amount>```")
        else :
            await ctx.send(f"{ctx.message.author.mention} you dont have manage messages perms")

    @commands.command()
    async def dm(self,ctx,u:discord.User,*,msg):
        if ctx.message.author.guild_permissions.administrator  or ctx.author.id in GODS:
            try:
                await u.send(msg)
            except Exception as e:
                await ctx.send(f"could not to send to {u.mention}")
                await ctx.send(f"||{e}||")
        else:
            await ctx.send(f"{ctx.message.author.mention} you dont have admin perms")

def setup(bot):
    bot.add_cog(Moderation(bot))
    print('---> MODERATION LOADED')
