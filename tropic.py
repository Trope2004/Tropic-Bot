from discord.ext import commands
import os

client = commands.Bot(command_prefix='#')

@client.event
async def on_ready():
    print('Der Bot is on')

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='Spieler')
    await client.add_roles(member, role)

@client.command(pass_context = True)
async def clear(ctx, number):
    number = int(number)
    counter = 0
    async for x in client.logs_from(ctx.message.channel, limit = number):
        if counter < number:
            await client.delete_message(x)
            counter += 1

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

client.run(os.getenv('TOKEN'))
