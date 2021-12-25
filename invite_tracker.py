import discord, json
# from discord import user

async def new_member(member):
    guild = member.guild
    with open('invites.json') as f:
        invites = json.load(f)

    invites_after = await guild.invites

    for i in invites_after:
        if i.uses > invites[i.code]["uses"]:
            inviter = invites[i.code]
            invites[i.code]["uses"] = i.uses
            print(f"{member.name} joined using" + {inviter["linked_user_id"]} + "'s code ({i.code}).")

            # Inviter's role
            role = discord.utils.get(guild.roles, id = inviter["linked_role_id"])
            await member.add_roles(role)

            # Own role
            r_name = member.name + "'s gang"
            role = await guild.create_role(name=r_name, mentionable = True)
            await member.add_roles(role)

            # Own invite link
            general_channel = discord.utils.get(guild.channels, id = 924048147825696840) # P.E.W's general channel
            new_invite = await general_channel.create_invite(unique = True, reason = r_name)

            # Save new role
            body = {
                        "uses": 0,
                        "linked_user_id": 0,
                        "linked_role_id": 0
                    }
            body["linked_user_id"] = member.id
            body["linked_role_id"] = role.id
            invites[new_invite.code] = body

            with open('invites.json', 'w') as json_file:
                json.dump(invites, json_file)
    return