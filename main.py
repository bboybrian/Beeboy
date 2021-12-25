#python3 -m pip install -U discord.py

import discord, requests, json
from discord import Client, Intents, Embed
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import os
from rgb import get_colour
import invite_tracker
import asyncio

bot = commands.Bot(command_prefix="")
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print('bzz bzz, {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # if message.author.id == 332845912873238530:
    #     await send_rules(message.channel)

async def send_rules(channel):
    await channel.send("https://cdn.discordapp.com/attachments/908738844042600478/918177317078057020/ServerChannelHeaders_Rules1.png")
    await channel.send("Obey or get spanked\n\n>>> :one: No spamming and no scamming\n:two: Don't abuse pings\n:three: No self-promotion or shilling\n:four: Keep it PMA, keep it BSJ")
    return

@bot.event
async def on_member_join(member):
    if(member.guild.id == 924048147221721149): # P.E.W Guild ID 
        invite_tracker.new_member(member)

@slash.slash(description="say the rules")
async def rules(ctx: SlashContext,arg):
    await ctx.send("https://cdn.discordapp.com/attachments/908738844042600478/918177317078057020/ServerChannelHeaders_Rules1.png")
    await ctx.send(">>> :one: No spamming and no scamming\n:two: Don't abuse pings\n:three: No self-promotion or shilling\n:four: Keep it PMA, keep it BSJ")
    return

body = {
            "max_age": 1800,
            "max_uses": 0,
            "target_application_id": "832012774040141894",
            "target_type": 2,
            "temporary": False,
            "validate": None
        }

auth = {
            "Authorization": "Bot NTU2ODg0NjM0MjQ4Njc1MzMw.XI59Ow.RbWPBtOMa_S2f1aQjbQcjdo8F7U",
            "Content-Type": "application/json",
            "X-Ratelimit-Precision": "millisecond"
        }
games = {
            "chess": "832012774040141894",
            "skribbl":"878067389634314250",
            "scrabble":"879863686565621790",
            "boggle":"879863976006127627",
            "checkers":"832013003968348200",
            "humanity":"879863881349087252",
            "watchparty":"880218394199220334",
            "poker":"755827207812677713",
            "amogus":"773336526917861400",
            "fishing":"814288819477020702",
            "fakeartist":"879864070101172255"
        }

# /play chess /play doodle /play checkers
@slash.slash(description="Play games in a voice channel")
async def play(ctx: SlashContext,arg):
    #await ctx.send("slash play detected")
    try:
        body["target_application_id"] = games[arg]
    except:
        embed = discord.Embed(title = "Available Games", description = "chess, checkers, skribbl, scrabble, boggle, humanity, poker, amogus,  fakeartist, watchparty", color = discord.Colour.green())
        await ctx.send(embed=embed)
        return
    try:
        voiceChannel = ctx.author.voice.channel
        if voiceChannel != None:
            url = f"https://discord.com/api/v9/channels/{voiceChannel.id}/invites"
            

            obj = json.dumps(body, separators=(',', ':'), ensure_ascii=True)
            code = (requests.post(url, data = obj, headers = auth))
            code = json.loads(code.text)["code"]
            invite = f"https://discord.gg/{code}"
            await ctx.send(invite)
        else:
            await ctx.send("Connect to VC you pepeg")
    except:
        await ctx.send("Connect to VC you 4head")

# async def rgb():
# 	guild = bot.get_guild(551625591305011201)
# 	role = discord.utils.get(guild.roles, name="rgb")
# 	print(role.color)
# 	col = 0xc80000
#
# 	while True:
# 		col = get_colour(col)
# 		await role.edit(colour=col)
# 		await asyncio.sleep(0.1)

# 	if message.content.startswith('u r a b'):
# 		await message.channel.send('me too thanks')
# 		await rgb()

bot.run('NTU2ODg0NjM0MjQ4Njc1MzMw.XI59Ow.RbWPBtOMa_S2f1aQjbQcjdo8F7U')