#python3 -m pip install -U discord.py

import discord, requests, json, os, asyncio
from discord import Client, Intents, Embed
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_components import DiscordComponents, Button
from rgb import get_colour
import invite_tracker.invite_tracker as invite_tracker

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
DiscordComponents(bot)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print('bzz bzz, {0.user}'.format(bot))

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

@bot.command()
async def a(ctx):
    await invite_tracker.test()

@bot.command()
async def b(ctx):
    buttons = [Button(label=" ", custom_id="1"), Button(label=" ", custom_id="2"),Button(label=" ", custom_id="3")]
    await ctx.send("Buttons!", components=buttons)

@bot.event
async def on_button_click(interaction):
    print("button_clicked")
    await interaction.respond(content=f"Button {interaction.component.custom_id} Clicked")

#region send functions

async def send_rules(channel):
    await channel.send("https://cdn.discordapp.com/attachments/908738844042600478/918177317078057020/ServerChannelHeaders_Rules1.png")
    await channel.send("Obey or get spanked\n\n>>> :one: No spamming and no scamming\n:two: Don't abuse pings\n:three: No self-promotion or shilling\n:four: Keep it PMA, keep it BSJ")
    return

#endregion

@bot.event
async def on_member_join(member):
    if member.guild.id == 924048147221721149: # P.E.W Guild ID  
        await invite_tracker.new_member(member)
        
@bot.event
async def on_member_remove(member):
    if member.guild.id == 924048147221721149: # P.E.W Guild ID 
        await invite_tracker.remove_member(member)

# /play
# region /play cache
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
# endregion
@slash.slash(
    #region /play details
    name = "play",
    description = "Play games in a voice channel",
    options = [
        create_option(
            name = "game",
            description = "Choose a game",
            required = True,
            option_type = 3,
            choices = [
                create_choice(
                    name = "Chess",
                    value = "chess"
                ),
                create_choice(
                    name = "Checkers",
                    value = "checkers"
                ),
                create_choice(
                    name = "Skribbl.io",
                    value = "skribbl"
                ),
                create_choice(
                    name = "Scrabble",
                    value = "scrabble"
                ),
                create_choice(
                    name = "Boggle",
                    value = "boggle"
                ),
                create_choice(
                    name = "Cards Against Humanity",
                    value = "humanity"
                ),
                create_choice(
                    name = "Poker",
                    value = "poker"
                ),
                create_choice(
                    name = "Amogus",
                    value = "amoguss"
                ),
                create_choice(
                    name = "Fishing",
                    value = "fishing"
                ),
                create_choice(
                    name = "Fake Artist",
                    value = "fakeartist"
                ),
                create_choice(
                    name = "YouTube watch party",
                    value = "watchparty"
                )
            ]
        )
    ]
    #endregion
)
async def play(ctx: SlashContext, game:str):
    #await ctx.send("slash play detected")
    try:
        body["target_application_id"] = games[game]
    except:
        embed = discord.Embed(title = "Available Games", description = "chess, checkers, skribbl, scrabble, boggle, humanity, poker, amogus, fishing, fakeartist, watchparty", color = discord.Colour.green())
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

# region rgb
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
# endregion

bot.run('NTU2ODg0NjM0MjQ4Njc1MzMw.XI59Ow.RbWPBtOMa_S2f1aQjbQcjdo8F7U')