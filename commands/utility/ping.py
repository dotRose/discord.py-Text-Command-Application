data = {
    "name":"ping",
    "description":"responds with pong"
}
async def execute(message, client):
    await message.channel.send('Pong!') 