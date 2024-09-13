data = {
    "name":"test",
    "description":"test commands"
}
async def execute(message, client):
    await message.channel.send('Send From Module')