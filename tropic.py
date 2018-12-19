import asyncio

import discord

import os

import SECRETS
import STATICS
from commands import cmd_hello

client = discord.Client()#

commands = {

    "Hello": cmd_hello,

}


@client.event
@asyncio.coroutine
def on_ready():
    print("Servers:\n")
    for s in client.servers:
        print(" - %s" % (s.name))
    yield from client.change_presence(game=discord.Game(name="> Tropic.tk <"))



@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith(STATICS.PRFIX):
        invoke = message.content[len(STATICS.PRFIX):].split(" ")[0]
        args = message.content.split(" ")[1:]
        if commands.__contains__(invoke):
            yield from commands.get(invoke).ex(args, message, client, invoke)
        else:
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.dark_green(), description=("Der Command `%s` existiert nicht." % invoke)))
            
client.run(str(os.environ.get("TOKEN")))
