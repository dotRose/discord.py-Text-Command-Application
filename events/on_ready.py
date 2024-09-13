name = 'on_ready'

async def execute(client):
    print(f'Logged in as {client.user}')