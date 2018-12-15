import discord
import youtube_dl
import json
import os
from discord.ext import commands
from itertools import cycle
import asyncio

client = commands.Bot(command_prefix='-t')
client.remove_command('help')

game = ['Es finden gerade Tests statt', 'Code > Hoster > Bot'.format(online), 'https://discord.gg/b2ZeERB']

async def change_status():
	await client.wait_until_ready()
	games = cycle(game)
	
	while not client.is_closed:
		current_games = next(games)
		await client.change_presence(status=discord.Status.dnd, game=discord.Game(name=current_games))
		await asyncio.sleep(3)
		
async def sql():
	await client.wait_until_ready()
	channel = client.get_channel('520196614384517130')
	)
	while not client.is_closed:
		await asyncio.sleep(2)
		await client.send_message(channel, "Connected to Hoster")
		mycursor = mydb.cursor()
		mycursor.execute("SELECT * FROM online")
		myresult = mycursor.fetchone()
		await asyncio.sleep(5)
		for ol in myresult:
			await client.send_message(channel, "Disconnected to Hoster")
			mycursor.close()
		
def check_queue(id):
	if queues[id] != []:
		player = queues[id].pop(0)
		players[id] = player
		player.start()

@client.event
async def on_ready():
	users = len(set(client.get_all_members()))
	servers = len(client.servers)
	channels = len([c for c in client.get_all_channels()])
	
	print("Connect to:")
	print("{} servers".format(servers))
	print("{} channels".format(channels))
	print("{} users".format(users))
	await client.change_presence(status=discord.Status.dnd, game=discord.Game(name='booting Bot...'))

@client.event
async def on_message_delete(message):
	log = client.get_channel("520196614384517130")
	content = message.content
	channel = message.channel
	author = message.author
	id = message.id
	embed = discord.Embed(
	title = 'Deleted Message',
	colour = discord.Colour.dark_red()
	)
	embed.add_field(name='Content:', value='`{}`'.format(content), inline=False)
	embed.add_field(name='Author:', value='`{}`'.format(author), inline=False)
	embed.add_field(name='In Channel:', value='`{}`'.format(channel), inline=False)
	embed.set_footer(text='ID: {}'.format(channel.id))
	
	await client.send_message(log, embed=embed)
	
@client.event
async def on_message_edit(before, after):
	log = client.get_channel("")
	before1 = before.content
	after1 = after.content
	channel = before.channel
	
	#await client.send_message(log, "Before: `{}` \nAfter: `{}` \nIn Channel: `{}` \nChannel ID: `{}`".format(before1, after1, channel, channel.id))
	
@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed = discord.Embed(
	title = 'Help Page',
	description = 'All Commands of this Bot',
	colour = discord.Colour.dark_purple()
	)
	
	embed.add_field(name='Help', value='-thelp', inline=False)
	embed.add_field(name='Echo', value='-techo <word>', inline=False)
	embed.add_field(name='Level', value='-tlevel', inline=False)
	embed.add_field(name='Ping', value='-tping', inline=False)
	embed.add_field(name='Join', value='-tjoin', inline=False)
	embed.add_field(name='Leave', value='-tleave', inline=False)
	embed.add_field(name='Play', value='-tplay <url>', inline=False)
	embed.add_field(name='Pause', value='-tpause', inline=False)
	embed.add_field(name='Resume', value='-tresume', inline=False)
	embed.add_field(name='Stop', value='-tstop', inline=False)
	embed.add_field(name='Queue', value='-tqueue <url>', inline=False)
	embed.add_field(name='Servers', value='-tserver', inline=False)
	embed.set_author(name='Steamarino', icon_url='https://cdn.discordapp.com/attachments/354668256675495937/520659862909353984/JPEG_20181201_165537.jpg')
	embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/354668256675495937/520659931679031296/20181129_172203.jpg')
	embed.set_footer(text='Help Page')
	
	await client.send_message(author, embed=embed)
	
@client.command()
async def echo(*args):
	output = ''
	for word in args:
		output += word
		output += ' '
	await client.say(output)
	
@client.command()
async def server():
	server = len(client.servers)
	servers = sorted(list(client.servers),
		key=lambda s: s.name.lower())
	await client.say("Server Nummer: {} \nServer List: {}".format(server, servers)) 
	
@client.command(pass_context=True)
async def level(ctx):
	with open('users.json', 'r') as f:
		users = json.load(f)
		lvl = users[ctx.message.author.id]['level']
		await client.send_message(ctx.message.channel, '{} you are at level {}'.format(ctx.message.author.mention, lvl))
	
@client.command(pass_context=True)
async def join(ctx):
	channel = ctx.message.author.voice.voice_channel
	await client.join_voice_channel(channel)
	await client.say("I`m joined your Voice Channel")
	
@client.command(pass_context=True)
async def leave(ctx):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	await voice_client.disconnect()
	await client.say("I`m leaving your Voice Channel")
	
@client.command(pass_context=True)
async def play(ctx, url):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
	players[server.id] = player
	player.start()
	await client.say("Now playing: {}".format(url))
	
@client.command(pass_context=True)
async def pause(ctx):
	message = ctx.message
	id = ctx.message.server.id
	players[id].pause()
	await client.add_reaction(message, "✔")
	
@client.command(pass_context=True)
async def stop(ctx):
	id = ctx.message.server.id
	players[id].stop()
	
@client.command(pass_context=True)
async def resume(ctx):
	id = ctx.message.server.id
	players[id].resume()
	
@client.command()
async def ping():
	await client.say("Pong!")
	
@client.command(pass_context=True)
async def logout(ctx):
	if 'Founder' in [r.name for r in ctx.message.author.roles]:
		await client.say("Logging out...")
		await client.logout()
	else:
			await client.say("Du hast keine Rechte dazu")
			
@client.command(pass_context=True)
async def queue(ctx, url):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
	
	if server.id in queues:
		queues[server.id].append(player)
	else:
		queues[server.id] = [player]
	await client.say("Added {} to Queue".format(url))
	
@client.command(pass_context=True)
async def kick(ctx, user: discord.Member):
	try:
		server = ctx.message.server
		await client.say(":boot: \nKicked: {} \nUserID: {}".format(user.name, user.id))
		await client.start_private_message(user)
		await client.send_message(user, "You are Kicked from {}".format(server))
		await client.kick(user)
	except discord.errors.Forbidden:
		await client.say("I'm not allowed to do that.")
	
@client.command(pass_context=True)
async def ban(ctx, user: discord.Member):
	server = ctx.message.server
	await client.say(":hammer: \nBanned: {} \nUserID: {}".format(user.name, user.id))
	await client.start_private_message(user)
	await client.send_message(user, "You are Banned from {}".format(server))
	await client.ban(user, 2)
	
@client.command(pass_context=True)
async def unban(ctx, user: discord.Member):
	try:
		server = ctx.message.server
		await client.say(":hammer: \nUnbanned: {} \nUserID: {}".format(user.name, user.id))
		await client.start_private_message(user)
		await client.send_message(user, "You are Unbanned from {}".format(server))
		await client.unban(server, user)
	except discord.errors.Forbidden:
		await client.say("I'm not allowed to do that.")
		
@client.command(pass_context=True)
async def banlist(ctx):
	server = ctx.message.server
	bans = list(client.get_bans(server))
	await client.say("Ban List: {}".format(bans))
	
client.loop.create_task(change_status())
client.run(os.getenv('TOKEN'))
