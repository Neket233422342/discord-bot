import discord
from discord.ext import commands
import asyncio
import json
import os
from itertools import cycle
import time

prefix = ","
TOKEN = "NTM4MzMxMjgxNDA3MDgyNTA4.DyyPnA.Chl42K27ZlkqRyPH0SU4KCs6tAA"

client = commands.Bot(command_prefix = ',')
status = ["Аноним гет рект", "аноним клиент гавно", "швэ"]
players = {}
os.chdir(r'./')
bypass_list = ['d1ck']
chat_filter = ["PINEAPPLE", "APPLE", "CHROME", "dick"]

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(1)

@client.event
async def on_ready():
    print("Bot was launched!")
    print("Discord bot by fantic232323!")
    print("Bot version 1337")

@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

        await update_data(users, member)

        #code

        with open('users.json', 'w') as f:
            json.dump(users, f)

@client.event
async def on_message(message):
    await client.process_commands(message)
    with open('users.json', 'r') as f:
        users = json.load(f)

        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message.channel)

        #code

        with open('users.json', 'w') as f:
            json.dump(users, f)

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1

async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp

async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await client.send_message(channel, '{} has leveled up to level {}'.format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end

@client.command()
async def logout():
    await client.logout()

@client.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title="Info about commands", colour= 0x00FF00)
    emb.add_field(name= "{}help".format(prefix), value="Shows this embed")
    emb.add_field(name="{}ban".format(prefix), value="To ban someone")
    await client.say(embed= emb)

@client.command()
async def ping():
    await client.say("пук")

@client.command(pass_context=True)
async def ban(ctx, user: discord.Member):
    await client.ban(user)

@client.command(pass_context = True)
async def clear(ctx, amout=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amout)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('messages was deleted!')

client.loop.create_task(change_status())
client.run(os.getenv('TOKEN'))
