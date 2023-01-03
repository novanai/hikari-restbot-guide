import asyncio
import os

import dotenv
import hikari

dotenv.load_dotenv()


CLIENT_ID = int(os.environ["CLIENT_ID"])
CLIENT_SECRET = os.environ["CLIENT_SECRET"]


def build_commands(app: hikari.impl.RESTClientImpl) -> list[hikari.api.CommandBuilder]:
    return [app.slash_command_builder("ping", "Ping the bot.")]


async def register() -> None:
    rest = hikari.RESTApp()
    await rest.start()

    async with rest.acquire(None) as app:
        token = await app.authorize_client_credentials_token(
            CLIENT_ID, CLIENT_SECRET, [hikari.OAuth2Scope.APPLICATIONS_COMMANDS_UPDATE]
        )

    async with rest.acquire(token.access_token, "Bearer") as app:
        commands = build_commands(app)

        await app.set_application_commands(
            CLIENT_ID,
            commands,
        )

    await rest.close()


asyncio.run(register())
