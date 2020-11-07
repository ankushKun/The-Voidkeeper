import discord
from discord.ext import commands
from discord.utils import get
import json
from collections import Counter 
from disputils import BotEmbedPaginator,BotConfirmation
import pyrebase
import collections
from decouple import config


firebase = pyrebase.initialize_app(json.loads(config("FIREBASE")))
db=firebase.database()

theme = { # CHANGE THESE ACCORDING TO ROLES
  'S':"S",
  'A':"A",
  'B':"B",
  'C':"C",
  'D':"D",
  'E':"E"
}

def get_class(points):
  if points>=80:
    return "S"
  elif points>=50:
    return "A"
  elif points>=30:
    return "B"
  elif points>=15:
    return "C"
  elif points>=5:
    return "D"
  elif points>=1:
    return "E"
  else:
    return "No"

GODS = [272285219942301696,728044189417209856,666578281142812673]

class Manager(commands.Cog):
  def __init__(self,bot):
    self.bot=bot

  @commands.command(aliases=["gp"])
  async def givepoint(self,ctx,u:discord.User=None,points=0):
    if ctx.author.id in GODS:
      if points==0 or u==None:
        e=discord.Embed(title="",description=f"{ctx.author.mention}\nusage : `,givepoint <mention> <amount>`\naliases : `gp`",color=0x00FFFF)
        await ctx.send(embed=e)
        return
      user_id=str(u.id)
      tp = db.child("TOTAL-POINTS").get().val()
      op = db.child("OLD-POINTS")
      if user_id in tp:
        op.child(user_id).set(tp[user_id])
        db.child("TOTAL-POINTS").child(user_id).set(tp[user_id]+points)
      else:
        op.child(user_id).set(0)
        db.child("TOTAL-POINTS").child(user_id).set(points)
      tp = db.child("TOTAL-POINTS").get().val()
      p = db.child("TOTAL-POINTS").get().val()[user_id]
      e=discord.Embed(title="",description=f"{u.mention} recieved {points} points\nTotal Points : {p}",color=0x00FFFF)
      await ctx.message.delete()
      await ctx.send(embed=e)


  @commands.command(aliases=["p"])
  async def points(self,ctx,u:discord.User=None):
    if u==None:
      u=ctx.author
    user_id=str(u.id)
    tp = db.child("TOTAL-POINTS").get().val()
    if user_id in tp:
      e=discord.Embed(title="",description=f"{u.mention} | {tp[user_id]} points | {theme[get_class(tp[user_id])]} Class",color=0x00FFFF)
    else:
      e=discord.Embed(title="",description=f"{u.mention} | 0 Points | No Class",color=0x00FFFF)
    await ctx.send(embed=e)

  @commands.command(aliases=["pl"])
  async def players(self,ctx):
    if ctx.author.id in GODS:
      
      c = db.child("TOTAL-POINTS").order_by_value().get().val()
      c = collections.OrderedDict(reversed(list(c.items())))
      c = list(c.items())
      embeds=[]
      for i in range(0,len(c),20):
        j=i
        dsc=""
        while j<i+20:
          try:
            dsc+=f"**Rank {j+1} | <@{c[j][0]}> | {c[j][1]} points | {theme[get_class(c[j][1])]} Class**\n"
            #print(dsc)
          except Exception as e:
            break
          j+=1
        emb = discord.Embed(title=f"All Players",description=dsc,color=0x00FFFF)
          
        embeds.append(emb)
                  
      paginator = BotEmbedPaginator(ctx, embeds)
      await paginator.run()

  @commands.command(aliases=["lb"])
  async def leaderboard(self,ctx):
    c = db.child("TOTAL-POINTS").order_by_value().limit_to_last(10).get().val()
    c = collections.OrderedDict(reversed(list(c.items())))
    c = list(c.items())
    lb=""
    for i in range(len(c)):
      if i<10:
        lb+=f"**Rank {i+1} | <@{c[i][0]}> | {c[i][1]} points | {theme[get_class(c[i][1])]} Class**\n"
      else:
        break
    emb = discord.Embed(title=f"Top 10 Players",description=lb,color=0x00FFFF)
    await ctx.send(embed=emb)


  @commands.command(aliases=["ne"])
  async def newevent(self,ctx,multiplier=1.0,*,name=""):
    if ctx.author.id in GODS:
      if name=="" or multiplier<=0:
        e=discord.Embed(title="",description=f"{ctx.author.mention}\nusage : `,newevent <multiplier> <event name>`\naliases : `ne`",color=0x00FFFF)
        await ctx.send(embed=e)
        return
      db.child("EVENT").child("NAME").set(name)
      db.child("EVENT").child("MULTIPLIER").set(multiplier)
      e=discord.Embed(title="",description=f"{ctx.author.mention} created new event called\n**{name}** with a {multiplier}x multiplier",color=0x00FFFF)
      await ctx.send(embed=e)
    
  @commands.command(aliases=["egp"])
  async def eventgivepoint(self,ctx,u:discord.User=None,points=0):
    if ctx.author.id in GODS:
      if u==None or points==0:
        e=discord.Embed(title="",description=f"{ctx.author.mention}\nusage : `,eventgivepoint <mention> <amount>`\naliases : `egp`",color=0x00FFFF)
        await ctx.send(embed=e)
        return
      user_id=str(u.id)
      ep = db.child("EVENT-POINTS").get().val()
      if ep!=None and user_id in ep:
        db.child("EVENT-POINTS").child(user_id).set(ep[user_id]+points)
      else:
        db.child("EVENT-POINTS").child(user_id).set(points)
      ep = db.child("EVENT-POINTS").get().val()
      e=discord.Embed(title="",description=f"{u.mention} recieved {points} points\nEvent Points : {ep[user_id]}",color=0x00FFFF)
      await ctx.message.delete()
      await ctx.send(embed=e)

  @commands.command(aliases=["elb"])
  async def eventleaderboard(self,ctx):
    c = db.child("EVENT-POINTS").order_by_value().get().val()
    if c==None:
      c={}
    else:
      c = collections.OrderedDict(reversed(list(c.items())))
      c = list(c.items())
    en = db.child("EVENT").child("NAME").get().val()
    ex = db.child("EVENT").child("MULTIPLIER").get().val()
    lb=""
    for i in range(len(c)):
      #if i<10:
      if True:
        if ex>1:
          lb+=f"**Rank {i+1} | <@{c[i][0]}> | {c[i][1]} x {ex} = {int(c[i][1]*ex)} points**\n"
        else:
          lb+=f"**Rank {i+1} | <@{c[i][0]}> | {c[i][1]} points**\n"
      else:
        break
    emb = discord.Embed(title=en,description=lb,color=0x00FFFF)
    await ctx.send(embed=emb)

  @commands.command(aliases=["att"])
  async def addtototal(self,ctx,ded=""):
    if ctx.author.id in GODS:
      ep = db.child("EVENT-POINTS").order_by_value().get().val()
      tp = db.child("TOTAL-POINTS").order_by_value().get().val()
      op = db.child("OLD-POINTS").get().val()
      #ep = list(ep.items())
      #print(ep)
      ex = en = db.child("EVENT").child("MULTIPLIER").get().val()
      if ep!=None and ded.lower()=="deduct":
        for id in tp:
          cl=get_class(tp[id])
          if cl=="S":
            db.child("TOTAL-POINTS").child(id).set(tp[id]-4)
          elif cl=="A":
            db.child("TOTAL-POINTS").child(id).set(tp[id]-3)
          elif cl=="B":
            db.child("TOTAL-POINTS").child(id).set(tp[id]-2)
          elif cl=="C":
            db.child("TOTAL-POINTS").child(id).set(tp[id]-1)
      tp = db.child("TOTAL-POINTS").order_by_value().get().val()
      ep = db.child("EVENT-POINTS").order_by_value().get().val()
      if ep != None:
        for id in ep:
          if id in tp:
            db.child("OLD-POINTS").child(id).set(tp[id])
            db.child("TOTAL-POINTS").child(id).set(int(tp[id]+ep[id]*ex))
          else:
            db.child("TOTAL-POINTS").child(id).set(int(ep[id]*ex))
      en = db.child("EVENT").child("NAME").get().val()
      emb = discord.Embed(title=en,description=f"Event Points added to Total Points\nUse `,updateclass` [uc] to update class roles",color=0x00FFFF)
      await ctx.send(embed=emb)
      db.child("EVENT-POINTS").remove()

  @commands.command(aliases=["cl"])
  async def classlog(self,ctx):
    new_class={}
    old_class={}
    tp = db.child("TOTAL-POINTS").order_by_value().get().val()
    op = db.child("OLD-POINTS").get().val()
    for id in tp:
      if not id in op:
        db.child("OLD-POINTS").child(id).set(0)
      new_class[id]=get_class(tp[id])
    op = db.child("OLD-POINTS").get().val()
    for id in op:
      old_class[id]=get_class(op[id])
    
    class_chng=""
    for id in new_class:
      if not new_class[id]==old_class[id]:
        pd=""
        if ord(new_class[id][0]) < ord(old_class[id][0]):
          pd = "promoted"
        else:
          pd = "demoted"
        if new_class[id]=="S":
          pd="promoted"
        if old_class[id]=="S" and new_class[id]!="S":
          pd="demoted"
        class_chng+=f"**<@{id}> {pd} to {theme[new_class[id]]} Class**\n"
    en = db.child("EVENT").child("NAME").get().val()
    emb = discord.Embed(title=en,description=f"{class_chng}",color=0x00FFFF)
    await ctx.send(embed=emb)

  @commands.command(aliases=["dl"])
  async def deletelogs(self,ctx,u:discord.User=None):
    if ctx.author.id in GODS:
      tp = db.child("TOTAL-POINTS").get().val()
      for id in tp:
        db.child("OLD-POINTS").child(id).set(tp[id])
      en = db.child("EVENT").child("NAME").get().val()
      emb = discord.Embed(title=en,description=f"deleted logs",color=0x00FFFF)
      await ctx.send(embed=emb)

  @commands.command()
  async def delete(self,ctx,u:discord.User):
    if ctx.author.id in GODS:

      confirmation = BotConfirmation(ctx, 0x00FFFF)
      await confirmation.confirm("Are you sure?")

      if confirmation.confirmed:
        await confirmation.update("Confirmed", color=0x00FFFF)
        db.child("TOTAL-POINTS").child(u.id).remove()
        db.child("OLD-POINTS").child(u.id).remove()
      else:
        await confirmation.update("Not confirmed", hide_author=True, color=0x00FFFF)
      
      emb = discord.Embed(title="",description=f"{u.mention}s data has been deleted",color=0x00FFFF)
      await ctx.send(embed=emb)

  @commands.command(aliases=["uc"])
  async def updateclass(self,ctx):
    if ctx.author.id in GODS:
      new_class={}
      old_class={}
      tp = db.child("TOTAL-POINTS").get().val()
      op = db.child("OLD-POINTS").get().val()
      en = db.child("EVENT").child("NAME").get().val()
      for id in tp:
        if not id in op:
          db.child("OLD-POINTS").child(id).set(0)
        new_class[id]=get_class(tp[id])
      op = db.child("OLD-POINTS").get().val()
      for id in op:
        old_class[id]=get_class(op[id])
      guild = ctx.guild
      class_id=[749656520064630924,749656432970039426,749656153214025798,749656040072544326,749655462479265862,749655929544245328]
      roles=[]
      for id in class_id:
        roles.append(get(ctx.guild.roles, id=id))
      tp = db.child("TOTAL-POINTS").get().val()
      
      emb_updating=discord.Embed(title=en,description=f"Updating roles",color=0x00FFFF)
      msg=await ctx.send(embed=emb_updating)
      for id in new_class:
        if not new_class[id]==old_class[id]:
          # Class update
          member = guild.get_member(int(id))
          #print(member)
          loading = get(ctx.message.guild.emojis, name="loading")
          emb_updating=discord.Embed(title=en,description=f"{loading} updating roles for {member}",color=0x00FFFF)
          await msg.edit(embed=emb_updating)
          
          for rl in roles:
            try:
              await member.remove_roles(rl)
              #print(f"removed role from {member}")
            except Exception as e:
              print(f"failed to remove role from {member} : {e}")
          cls = get_class(tp[id])
          try:
            if cls=="S":
              await member.add_roles(roles[0])
            elif cls=="A":
              await member.add_roles(roles[1])
            elif cls=="B":
              await member.add_roles(roles[2])
            elif cls=="C":
              await member.add_roles(roles[3])
            elif cls=="D":
              await member.add_roles(roles[4])
            elif cls=="E":
              await member.add_roles(roles[5])
            #print(f"added role to {member}")
          except Exception as e:
            print(f"filed to give role to {member} : {e}")
      done = discord.Embed(title=en,description=f"Done updating roles",color=0x00FFFF)
      await msg.edit(embed=done)

  
    
def setup(bot):
  bot.add_cog(Manager(bot))
  print('---> MANAGER LOADED')
  
  #top = db.child("TOTAL-POINTS").order_by_value().limit_to_last(10).get().val()
  

