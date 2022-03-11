import discord
from discord.ext import commands
import logging
import random
import datetime
import roller

admin_ids = [384729201544134659]
#Using own discord id, as I currently do not know how to check for permissions - will update

#The following will write any error logs to a file.
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = commands.Bot(command_prefix='>', case_insensitive=True)
client.help_command = None


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print("-----------------")


@client.command()
async def hello(ctx):
    print_log(ctx, '>hello')
    if ctx.author.id == admin_ids[0]:
        await ctx.send(f'Greetings, Creator.')
    else:
        await ctx.send(f'Hello, {ctx.author.mention}')
    print("-----------------")


@client.command()
async def help(ctx):
    print_log(ctx, '>helpme')
    await ctx.send(f'''**[Help Menu]**
*>hello*
    Sends a hello message to the user.
    
*>roll*
    Rolls (several) die and gives you the result.
    Format your message as ">roll [mode][dice count]d[dice faces]
    [mode] should be "ex", "excont", or be empty.
         -"ex" (exploding) will cause maximum rolls to add an extra die to the pool
         -"exc" (exploding continuously) will do the same, but extra rolls become subject to the same rule.
         -Leaving it blank or as anything else will make it a regular roll.
    
*>help*
    This one is obvious.

*>kill*
    Turns off the bot.''')
    print("-----------------")


@client.command()
async def roll(ctx, string: str):
    print_log(ctx, '>roll')
    print(string)
    if string.startswith("n "):
        classic = False
        string = string[6::]
    else:
        classic = True
    string = message_clean(string)

    try:
        result = roller.main(string,classic)
        print(result)
        await ctx.send(result)
    except:
        await ctx.send("""Something went wrong!
The output is likely outside of the character limit, try rolling smaller quantities of dice."""
                       )
    print("-----------------")


@client.command()
async def kill(ctx):
    print_log(ctx, '>kill')
    if ctx.author.id in admin_ids:
        await ctx.send("Going offline, goodbye!")
        await client.change_presence(status=discord.Status.offline)
        quit()
    else:
        await ctx.send("Sorry, only admins can use this command.")
    print("-----------------")


#########################


def print_log(ctx, command):
    print(command)
    print(f"{ctx.author.name}    -    {ctx.author.id}")
    print(datetime.datetime.now())
    print(ctx.channel)


def message_clean(message):
    messsage = message.replace("'","").replace('"','').replace("(","").replace(")", "").strip()
    return message.lower()
