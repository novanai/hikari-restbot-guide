import asyncio
import datetime
import os

import dotenv
import hikari

dotenv.load_dotenv()

CLIENT_ID = int(os.environ["CLIENT_ID"])
CLIENT_SECRET = os.environ["CLIENT_SECRET"]


def ping(event: hikari.CommandInteraction) -> hikari.api.InteractionMessageBuilder:
    return event.build_response().set_content("Pong!")


def userinfo(event: hikari.CommandInteraction) -> hikari.api.InteractionMessageBuilder:
    assert event.guild_id is not None

    if event.resolved:
        if members := list(event.resolved.members.values()):
            member = members[0]
        else:
            return event.build_response().set_content(
                "That user is not in this server."
            )
    else:
        member = event.member

    assert member is not None
    assert event.member is not None

    created_at = int(member.created_at.timestamp())
    joined_at = int(member.joined_at.timestamp())

    roles = [f"<@&{role}>" for role in member.role_ids if role != event.guild_id]

    embed = (
        hikari.Embed(
            title=f"Member Info - {member.display_name}",
            description=f"ID: `{member.id}`",
            colour=0x3B9DFF,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
        )
        .set_footer(
            text=f"Requested by {event.member}",
            icon=event.member.display_avatar_url,
        )
        .set_thumbnail(member.avatar_url)
        .add_field(
            "Bot?",
            "Yes" if member.is_bot else "No",
            inline=True,
        )
        .add_field(
            "Created account on",
            f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
            inline=True,
        )
        .add_field(
            "Joined server on",
            f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
            inline=True,
        )
        .add_field(
            "Roles",
            ", ".join(roles) if roles else "No roles",
            inline=False,
        )
    )

    return event.build_response().add_embed(embed)


async def on_interaction(
    event: hikari.CommandInteraction,
) -> hikari.api.InteractionMessageBuilder:  # type: ignore
    if event.command_name == "ping":
        return ping(event)
    elif event.command_name == "userinfo":
        return userinfo(event)


async def get_token() -> str:
    rest = hikari.RESTApp()
    await rest.start()

    async with rest.acquire(None) as app:
        token = await app.authorize_client_credentials_token(
            CLIENT_ID, CLIENT_SECRET, [hikari.OAuth2Scope.APPLICATIONS_COMMANDS_UPDATE]
        )

    await rest.close()
    return token.access_token


token = asyncio.run(get_token())

bot = hikari.RESTBot(token, "Bearer", banner=None)
bot.set_listener(hikari.CommandInteraction, on_interaction)
bot.run()
