#python3 -m pip install -U discord.py

import discord, requests, json
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_components import DiscordComponents
# from rgb import get_colour
import invite_tracker.invite_tracker as invite_tracker
import cache as cc

with open('token.txt') as f:
        token = f.read()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
DiscordComponents(bot)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print('bzz bzz, {0.user}'.format(bot))

@bot.event
async def on_button_click(interaction):
    if interaction.message.id == 924679405987561523:
        print("button_click")
        await prepend_emoji(interaction.author, interaction.component.label)
        await interaction.respond(content="Changed! Sidebar takes a while to update")
        await update(interaction.guild)

async def update(guild):
    # Update Leaderboard
    await update_leaderboard(guild)

    # Shift bots to bottommost role
    role = guild.get_role(924250286468526080) # P.E.W 'Bot' role ID
    role.edit(position = 0)
    return

#region send functions
@bot.command()
async def send_rules(ctx):
    await ctx.send(cc.rules1)
    await ctx.send(cc.rules2, components = cc.emoji_buttons)
    await ctx.send("Choose gang colour with: ```fix\n/colour [HEX]```")
    return

leaderboard = 924737070138818600 # Message ID of leaderboard message
@bot.command()
async def update_leaderboard(guild):
    print("update_leaderboard")
    try:
        all_gangs = {}
        all_roles = await guild.fetch_roles()
        for role in all_roles:
            if "gang" in role.name:
                await role.edit(hoist = False)
                if len(role.members) > 0: # 0 for beta only, afterwards 2
                    all_gangs[role.name] = len(role.members)
        all_gangs = sorted(all_gangs.items(), key=lambda x:x[1])
        all_gangs.reverse()
        await hoist_leaderboard(all_roles, all_gangs)

        # Edit message
        leaderboard_channel = guild.get_channel(924692245746184242) # P.E.W's leaderboard channel
        l_msg = await leaderboard_channel.fetch_message(leaderboard)
        await l_msg.edit(content = cc.fill_leaderboard(all_gangs))
        print("leaderboard updated")
        # await ctx.send(cc.leaderboard_h)
        # await ctx.send(cc.blank_banner)
        # await ctx.send(cc.fill_leaderboard(all_gangs))
    except:
        print("update_leaderboard failed")
    return

async def hoist_leaderboard(rlist, llist):
    for i in range(min(3,len(llist))):
        for role in rlist:
            if role.name == llist[i][0]:
                print(role.name)
                await role.edit(hoist=True)
                break
#endregion

@bot.event
async def on_member_join(member):
    if member.guild.id == 924048147221721149: # P.E.W Guild ID  
        await invite_tracker.new_member(member)
        await update(member.guild)

@bot.event
async def on_member_remove(member):
    if member.guild.id == 924048147221721149: # P.E.W Guild ID 
        await invite_tracker.remove_member(member)
        await update(member.guild)

# region prepend emoji
async def prepend_emoji(member, emoji):
    try:
        role = invite_tracker.find_linked_role(member)
        new_name = emoji + " " + member.name + "'s gang"
        await role.edit(name=new_name) 
    except:
        print("prepend_emoji failed")
    return
# endregion

# region /colour
@slash.slash(description="Change gang colour to a HEX colour code")
async def colour(ctx:SlashContext, hex):
    try:
        role = invite_tracker.find_linked_role(ctx.author)
        hex = int(hex, 16)
        print(hex)
        await role.edit(colour=hex)
        await ctx.send("Colour changed!")
        await update(ctx.guild)
    except:
        await ctx.send("Invalid colour hex")
    return
# endregion

# region /play
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
            "Authorization": "Bot " + token,
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
)
async def play(ctx: SlashContext, game:str):
    #await ctx.send("slash play detected")
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
# endregion

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

bot.run(token)