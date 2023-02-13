# python3 -m pip install -U discord.py
# REFRESH INVITES.JSON FROM EPIKHOST BEFORE DOING ANYTHING

import discord, requests, json
from discord.ext import commands
# from discord_slash import SlashCommand, SlashContext
# from discord_slash.utils.manage_commands import create_choice, create_option
# from discord_components import DiscordComponents
# from rgb import get_colour
import invite_tracker.invite_tracker as invite_tracker
import cache as cc

t = {}
with open("tokens.env") as f:
    for line in f:
        if line.startswith('#') or not line.strip(): # Ignore comments
            continue
        key, value = line.strip().split('=', 1)
        t[key] = value

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

#region debug functions
@bot.command()
@commands.has_role('Developer')
async def send_rules(ctx):
    await ctx.send(cc.rules1)
    await ctx.send(cc.rules2, components = cc.emoji_buttons)
    await ctx.send("Choose gang colour with: ```fix\n/colour [HEX]```")
    return

@bot.command()
@commands.has_role('Developer')
async def move_role(ctx, role_id: int, pos: int):
    role = ctx.guild.get_role(role_id)
    await ctx.send("Role id: " + str(role_id))
    await ctx.send("Pos: " + str(pos))
    await ctx.send("Role name: " + role.name)
    try:
        await role.edit(position=pos)
        await ctx.send("Role moved")
    except:
        await ctx.send("Role not moved")

@bot.command()
@commands.has_role('Developer')
async def dev_update(ctx):
    await update(ctx.guild)

@bot.command()
@commands.has_role('Developer')
async def purge(ctx):
    msgs = await ctx.channel.history(limit=100).flatten()
    await ctx.channel.delete_messages(msgs)
    print("deleted 100 most recent messages")
#endregion

@bot.event
async def on_ready():
    print('bzz bzz, {0.user}'.format(bot))

# @bot.event
# async def on_button_click(interaction):
#     if interaction.message.id == t["button_message"]:
#         print("button_click")
#         await prepend_emoji(interaction.author, interaction.component.label)
#         await interaction.respond(content="Changed! Sidebar takes a while to update")
#         await update(interaction.guild)

# async def prepend_emoji(member, emoji):
#     try:
#         role = invite_tracker.find_linked_role(member)
#         new_name = emoji + " " + member.name + "'s gang"
#         await role.edit(name=new_name) 
#     except:
#         print("prepend_emoji failed")
#     return

# async def update(guild):
#     # Shift 'Bot' to bottommost role
#     role = guild.get_role(t["PEW_bot_role"]) # P.E.W 'Bot' role ID
#     if role.position > 1:
#         await role.edit(position = 1)

#     # Update Leaderboard
#     await update_leaderboard(guild)
#     return

# leaderboard = t["leaderboard_message"] # Message ID of leaderboard message
# async def update_leaderboard(guild):
#     print("update_leaderboard")
#     try:
#         all_gangs = {}
#         all_roles = await guild.fetch_roles()
#         for role in all_roles:
#             if "gang" in role.name:
#                 await role.edit(hoist = False)
#                 if len(role.members) > 2: # 0 for beta only, afterwards 2
#                     all_gangs[role.name] = len(role.members)
            
#         # Edit message
#         leaderboard_channel = guild.get_channel(t["leaderboard_channel"]) # P.E.W's leaderboard channel
#         l_msg = await leaderboard_channel.fetch_message(leaderboard)
#         if all_gangs == {}:
#             await l_msg.edit(content ="Only gangs with 3+ members are shown")
#         else:
#             all_gangs = sorted(all_gangs.items(), key=lambda x:x[1])
#             all_gangs.reverse()
#             await hoist_leaderboard(all_roles, all_gangs)
#             await l_msg.edit(content = cc.fill_leaderboard(all_gangs))  
#         print("leaderboard updated")
#         # await ctx.send(cc.leaderboard_h)
#         # await ctx.send(cc.blank_banner)
#         # await ctx.send(cc.fill_leaderboard(all_gangs))
#     except:
#         print("update_leaderboard failed")
#     return

# async def hoist_leaderboard(rlist, llist):
#     n_gangs = len(llist)
#     for i in range(min(3,n_gangs)):
#         for role in rlist:
#             if role.name == llist[i][0]:
#                 print(role.name)
#                 await role.edit(hoist=True)
#                 await role.edit(position = n_gangs + 1 - i) # +1 for the Bot role

#                 # Private category for top 3 gangs
#                 k = "gang_cat_" + str(i)
#                 category = role.guild.get_channel(t[k])
#                 await category.edit(name = role.name)
#                 await category.set_permissions(role, cc.permissions2)
#                 boss = invite_tracker.find_linked_member(role)
#                 await category.set_permissions(boss, cc.permissions)
#                 break

# region invite_tracker functions
# @bot.event
# async def on_member_join(member):
#     if member.guild.id == t["PEW_guild"]: # P.E.W Guild ID 
#         if member.id == t["bboybrian"]: # Auto dev myself
#             role = member.guild.get_role(t["PEW_dev_role"])
#             await member.add_roles(role)
#         await invite_tracker.new_member(member)
#         await update(member.guild)

# @bot.event
# async def on_member_remove(member):
#     if member.guild.id == t["PEW_guild"]: # P.E.W Guild ID 
#         await invite_tracker.remove_member(member)
#         await update(member.guild)

# @bot.event
# async def on_invite_create(invite):
#     if invite.guild.id == t["PEW_guild"]: # P.E.W Guild ID 
#         if invite.inviter.id != t["beeboy"]: # Bee boy's ID
#             await invite.delete(reason = "unmanaged invite created")
#             print("deleted stray invite")


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
    except:
        await ctx.send("Invalid colour hex")

    try:
        await update(ctx.guild)
    except:
        print("colour update() failed")
    return
# endregion

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
            "Authorization": "Bot " + t["token"],
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

bot.run(t["token"])