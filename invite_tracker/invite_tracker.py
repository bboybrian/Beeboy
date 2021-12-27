import discord, json

def find_linked_role(member):
    with open('invite_tracker/invites.json') as f:
            invites = json.load(f)
    for i in invites:
        if invites[i]["linked_user_id"] == member.id:
            role = member.guild.get_role(invites[i]["linked_role_id"])
            return role

async def new_member(member):
    print("P.E.W new_member")
    guild = member.guild
    with open('invite_tracker/invites.json') as f:
        invites = json.load(f)

    invites_after = await guild.invites()
    for i in range(len(invites_after)):
        if invites_after[i].uses > invites[invites_after[i].code]["uses"]:
            j = invites_after[i].code
            inviter = invites[j]["linked_role_id"]
            invites[j]["uses"] = invites_after[i].uses
            print(f"{member.name} joined using code ({j}).")

            # Inviter's role
            role = guild.get_role(inviter)
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
            body["parent_code"] = j
            invites[new_invite.code] = body

            with open('invite_tracker/invites.json', 'w') as json_file:
                json.dump(invites, json_file)

            break
    return

async def remove_member(member):
    print("P.E.W remove_member")
    guild = member.guild
    print("id: " + str(member.id))
    if guild.get_member(member.id):
        print(f"{member.name} did not leave guild")
        return

    with open('invite_tracker/invites.json') as f:
        invites = json.load(f)
    
    for i in invites:
        if invites[i]["linked_user_id"] == member.id:
            # Legacy role members
            old_role = guild.get_role(invites[i]["linked_role_id"])
            try:
                new_role = guild.get_role(invites[invites[i]["parent_code"]]["linked_role_id"])
            except:
                print("old_role has no parent")
                return

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
            announcement = (f"{member.name} has left the server.\n<@&{old_role.id}> {member.name}'s gang will now be absorbed into {new_role.name}!")
            general_channel = guild.get_channel(924048147825696840) # P.E.W's general channel
            await general_channel.send(announcement)

            # Apply role change
            for m in old_role.members:
                await m.remove_roles(old_role, reason = member.name + " left the server")
                await m.add_roles(new_role, reason = "Subsumed by parent gang")

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
        else:
            print("member had no linked invite")
            return