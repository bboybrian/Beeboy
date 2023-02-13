import discord, requests, json
from discord.ext import commands
import asyncio

import os
import openai

import cache as cc
from rgb import get_colour

# Read environment variables from file
E = {}
with open("tokens.env") as f:
    for line in f:
        if line.startswith('#') or not line.strip(): # Ignore comments
            continue
        key, value = line.strip().split('=', 1)
        E[key] = value

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())
openai.api_key = E["openAI"]
openai.Model.list()

@bot.event
async def on_ready():
    print('bzz bzz, {0.user}'.format(bot))

# Activity settings
body = {
            "max_age": 1800,
            "max_uses": 0,
            "target_application_id": "832012774040141894",
            "target_type": 2,
            "temporary": False,
            "validate": None
        }

auth = {
            "Authorization": "Bot " + E["token"],
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


@bot.slash_command(
    name = "play",
    description = "Play games in a voice channel",
)

async def play(
    ctx: discord.ApplicationContext,
    game: discord.Option(str, "What game?"),
):
    try:
        body["target_application_id"] = games[game]
    except:
        await ctx.send(embed=cc.slashplay_embed)
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

# /rgb
# Makes the role "rgb" change to a visually different, random color every few seconds
@bot.slash_command(
    name = "rgb",
    # description = "Play games in a voice channel",
)
async def rgb(
    ctx: discord.ApplicationContext
):
    try:
        guild = bot.get_guild(551625591305011201)
        role = discord.utils.get(guild.roles, name="rgb")
        print(role.color)
        col = 0xc80000

        while True:
            col = get_colour(col)
            await role.edit(colour=col)
            await asyncio.sleep(3)

    except:
        await ctx.send("Something went wrong")

# /img [prompt]
# Uses openAI to generate an image using the input prompt
@bot.slash_command(
    name = "img",
    description = "AI generated image from a prompt",
)

async def img(
    ctx: discord.ApplicationContext,
    prompt: discord.Option(str, "What do you want to see?"),
):
    try:
        p = prompt
        await ctx.send("Generating images...")
        response = openai.Image.create(
            prompt=p,
            n=1,
            size="1024x1024"
        )
        for image in response["data"]:
            await ctx.send(image["url"])
    except:
        await ctx.send("Something went wrong")

bot.run(E["token"])