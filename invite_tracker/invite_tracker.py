import discord, json
from discord.channel import DMChannel

def find_linked_role(member):
    with open('invite_tracker/invites.json') as f:
            invites = json.load(f)
    for i in invites:
        if invites[i]["linked_user_id"] == member.id:
            role = discord.utils.get(member.guild.roles, id = invites[i]["linked_role_id"])
            return role

async def new_member(member):
    print("P.E.W new_member")
    guild = member.guild
    with open('invite_tracker/invites.json') as f:
        invites = json.load(f)

    invites_after = await guild.invites()

    for i in invites_after:
        if i.uses > invites[i.code]["uses"]:
            inviter = invites[i.code]
            invites[i.code]["uses"] = i.uses
            print(f"{member.name} joined using code ({i.code}).")

            # Inviter's role
            role = discord.utils.get(guild.roles, id = inviter["linked_role_id"])
            await member.add_roles(role)

            # Own role
            r_name = member.name + "'s gang"
            role = await guild.create_role(mentionable=True, name=r_name)
            await member.add_roles(role)

            # Own invite link
            general_channel = guild.get_channel(924048147825696840) # P.E.W's general channel
            new_invite = await general_channel.create_invite(unique = True, reason = r_name)

            # PM the user his/her invite link
            message = await member.send("Use this private code to invite friends to P.E.W:\ndiscord.gg/" + new_invite.code)
            await message.pin()

            # Save new role
            body = {
                        "uses": 0,
                        "linked_user_id": 0,
                        "linked_role_id": 0,
                        "parent_code": 0
                    }
            body["linked_user_id"] = member.id
            body["linked_role_id"] = role.id
            body["parent_code"] = i.code
            invites[new_invite.code] = body

            with open('invite_tracker/invites.json', 'w') as json_file:
                json.dump(invites, json_file)

            break
    return

async def remove_member(member):
    print("P.E.W remove_member")
    guild = member.guild
    with open('invite_tracker/invites.json') as f:
        invites = json.load(f)
    
    for i in invites:
        if invites[i]["linked_user_id"] == member.id:
            break
    
    print("i: " + i)

    # Legacy role members
    old_role = discord.utils.get(guild.roles, id = invites[i]["linked_role_id"])
    new_role = discord.utils.get(guild.roles, id = invites[invites[i]["parent_code"]]["linked_role_id"])

    # Delete pinned message in member's DM
    try:
        pins = await member.dm_channel.pins()
        for p in pins:
            if p.author != member:
                await p.delete()
                break
    except:
        print("DM Channel not found / no message pinned")

    # Announcement to old_role holders
    announcement = (f"{member.name} has left the server.\n<@&{old_role.id}> will now be absorbed into {new_role.name}!")
    general_channel = guild.get_channel(924048147825696840) # P.E.W's general channel
    await general_channel.send(announcement)

    # Apply role change
    for m in old_role.members:
        m.remove_roles(old_role, reason = member.name + " left the server")
        m.add_roles(new_role, reason = "Subsumed by parent gang")

    # Delete old role & invite
    await old_role.delete()
    all_invites = await guild.invites()
    for inv in all_invites:
        if inv.code == i:
            await inv.delete()
            break
    del invites[i]
    with open('invite_tracker/invites.json', 'w') as json_file:
        json.dump(invites, json_file)

    return