import json

async def get_invites(bot):
    invites = {}
    for guild in bot.guilds:
        invites[guild.id] = await guild.invites()

    with open('invites.json', 'w') as json_file:
        json.dump(invites, json_file)
    return

def find_invite(invites_, code):
    for invite in invites_:
        if invite.code == code:
            return invite

async def new_member(member):
    guild = member.guild
    with open('invites.json') as f:
        invites = json.load(f)

    invites_before = invites[guild.id]
    invites_after = await guild.invites

    for invite in invites_before:
        if invite.uses < find_invite(invites_after, invite.code).uses:
            print(f"{member.name} joined using {invite.inviter}'s code ({invite.code}).")
    
    invites[guild.id] = invites_after
    with open('invites.json', 'w') as json_file:
        json.dump(invites, json_file)
    return