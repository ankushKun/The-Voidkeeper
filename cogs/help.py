import discord
from discord.ext import commands

help_desc="""
**prefix : ,
`command <variables>` [aliases] description

**__Public Commands__**
`leaderboard` [lb] shows the list of top 10 players
`eventleaderboard` [elb] list of players in an event
`points <mention>` [p] check the points of a user
`classlog` [cl] view rank logs

**__Private Commands__**
`givepoint <mention> <amount>` [gp] give/take points from players
`players` list of all players
`newevent <multiplier> <event name>` [ne] creates a new event(will also erase all info from the previous event)
`eventgivepoint <mention> <amount>` [egp] give/take points from players in an ongoing event
`addtototal` [att] adds points of players from event to total points(will also clear the points from the event and give players their class roles)
`updateclass` [uc] will update the roles of those whose class has been changed
`deletelogs` [dl] deletes the rank logs
`delete <mention>` deletes a players data from the database

**__Moderation__**
`purge <amount>` deletes messages from the chat
`announce <announcement>` sends a DM to all members of the server
`dm <mention user> <message>` sends a DM to the mentioned user

developed by `weeblet~kun#1193`**
"""

class Help(commands.Cog):
  def __init__(self,bot):
    self.bot=bot

  @commands.command()
  async def help(self,ctx):
    e=discord.Embed(title="Need Help?",description=help_desc,color=0x00FFFF)
    await ctx.send(embed=e)

  @commands.command()
  async def ping(self,ctx):
    await ctx.send(f'Pong! {round(self.bot.latency, 2)*1000}ms.')

def setup(bot):
  bot.add_cog(Help(bot))
  print('---> HELP LOADED')
