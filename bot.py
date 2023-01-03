import asyncio
import os

import dotenv
import hikari

dotenv.load_dotenv()

CLIENT_ID = int(os.environ["CLIENT_ID"])
CLIENT_SECRET = os.environ["CLIENT_SECRET"]


async def on_inter(
    event: hikari.CommandInteraction,
) -> hikari.api.InteractionMessageBuilder:
    res = event.build_response().set_content("Pong!")
    return res


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
bot.set_listener(hikari.CommandInteraction, on_inter)
bot.run()
