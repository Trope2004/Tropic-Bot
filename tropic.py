import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
  print("I am ready!")
  
@bot.command(pass_context=True)
async def promote(ctx, user: discord.Member, role: discord.Role):
    for r in ctx.message.author.roles:
        if r.name == "High Rank" or r.name == "Super Rank":
            await(bot.add_roles(user,role))
            await(bot.say("Congrats! {} was promoted to {}!".format(user.name,role)))
            break
      
@bot.command(pass_context=True)
async def demote(ctx, user: discord.Member, role: discord.Role):
    for r in ctx.message.author.roles:
        if r.name == "High Rank" or r.name == "Super Rank":
            await(bot.remove_roles(user,role))
            await(bot.say("{} was demoted from {}.".format(user.name,role)))
            break
      
bot.run(os.environ["bot_token"
