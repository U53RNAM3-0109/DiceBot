#Librarian

import discord
from discord.ext import commands
import logging
import datetime
import csv

#The following will write any error logs to a file.
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Sets up bot
client = commands.Bot(command_prefix='?', case_insensitive=True)
client.help_command = None

#Runs command when ready
@client.event
async def on_ready():
    print("Loading values.")
    global channel_names

    channel_names = {}

    #restore_channel_ids('channelidsDict.csv')
    
    print(f"{client.user} is online.")
    print("--------------------------")

#Adds a new channel to the "bookshelf"
@client.command()
async def addshelf(ctx, channel_name : str):
    channel_names[channel_name] = ctx.channel.id

#Sends a message to a channel
@client.command()
async def contact(ctx, name : str, message : str):
    try:
        channel = client.get_channel(channel_names[name])
        await channel.send(message)
    except KeyError:
        await ctx.send("That channel does not exist in the Library database.")

#Kills the bot
@client.command()
@commands.is_owner()
async def kill(ctx):
    save_channel_ids('channelidsDict.csv')
    await client.change_presence(status=discord.Status.offline)
    await ctx.send("Going offline. Goodbye.")
    quit()

#########################
#Helper functions

def print_log(ctx, command):
    print(command)
    print(f"{ctx.author.name}    -    {ctx.author.id}")
    print(datetime.datetime.now())
    print(ctx.channel)


def message_clean(message):
    messsage = message.replace("'","").replace('"','').replace("(","").replace(")", "")
    return message.lower()

def restore_channel_ids(filename):
    channel_names = {}

    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        channel_names = {row[0]:row[1] for row in reader}

def save_channel_ids(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for i in channel_names:
            row = [i, channel_names[i]]
            writer.writerow(row)


##########################

client.run('OTA0MzU2ODU1NDk5ODc4NDgw.YX6V9A.BEwBNu4_YW9xgq2XFCrcaI3Bci4')
