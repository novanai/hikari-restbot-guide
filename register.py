import asyncio
import os

import dotenv
import hikari

dotenv.load_dotenv()


CLIENT_ID = int(os.environ["CLIENT_ID"])
CLIENT_SECRET = os.environ["CLIENT_SECRET"]


def build_commands(app: hikari.impl.RESTClientImpl) -> list[hikari.api.CommandBuilder]:
    ping = app.slash_command_builder("ping", "Ping the bot.")

    userinfo = (
        app.slash_command_builder("userinfo", "Get info on a server member.")
        .add_option(
            hikari.CommandOption(
                type=hikari.OptionType.USER,
                name="user",
                description="The user to get information about.",
            )
        )
        .set_is_dm_enabled(False)
    )

    return [ping, userinfo]


async def register() -> None:
    app = hikari.RESTApp()
    await app.start()

    async with app.acquire(None) as rest:
        token = await rest.authorize_client_credentials_token(
            CLIENT_ID, CLIENT_SECRET, [hikari.OAuth2Scope.APPLICATIONS_COMMANDS_UPDATE]
        )

    async with app.acquire(token.access_token, "Bearer") as rest:
        commands = build_commands(rest)

        await rest.set_application_commands(
            CLIENT_ID,
            commands,
        )

    await app.close()


asyncio.run(register())
