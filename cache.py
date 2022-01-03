import discord
from discord_components import Button

leaderboard_h = "https://i.imgur.com/bJEB4B8.png"
blank_banner = "https://i.imgur.com/ESYw3HE.png"

def fill_leaderboard(llist):
    leaderboard = ""
    i = 0
    for l in llist:
        v = ""
        if i == 0:
            v = "🥇"
        if i == 1:
            v = "🥈"
        if i == 2:
            v = "🥉"
        leaderboard += v + " " + l[0] + "\t-\t" + str(l[1]) + "\n"
        i += 1
    return leaderboard

permissions = discord.Permissions(permissions=1088840793936) # For the boss
permissions2 = discord.Permissions(permissions=1071631433280) # For the members

emoji_buttons = [
    [Button(label="🐸"), Button(label="🥶"),Button(label="🏹"),Button(label="❤️‍🔥"), Button(label="🎲")],
    [Button(label="👀"), Button(label="🍉"),Button(label="💦"),Button(label="⛄"), Button(label="💎")],
    [Button(label="👨‍🦽"), Button(label="🍆"),Button(label="🎺"),Button(label="💰"), Button(label="🐵")],
    [Button(label="👅"), Button(label="💀"),Button(label="🎸"),Button(label="🤖"), Button(label="🎮")],
    [Button(label="🍨"), Button(label="👺"),Button(label="⛏"),Button(label="🌷"), Button(label="🐼")]
    ]

rules1 = "https://cdn.discordapp.com/attachments/908738844042600478/918177317078057020/ServerChannelHeaders_Rules1.png"
rules2 = "Obey or get spanked\n\n> :one: No spamming and no scamming\n> :two: Don't abuse pings\n> :three: No self-promotion or shilling\n> :four: Keep it PMA, keep it BSJ\n\nChoose gang sign:"

slashplay_embed = discord.Embed(title = "Available Games", description = "chess, checkers, skribbl, scrabble, boggle, humanity, poker, amogus, fishing, fakeartist, watchparty", color = discord.Colour.green())
