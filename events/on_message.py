name = 'on_message'
once = False  # Optional, defaults to False

async def execute(client, message):
    if message.author == client.user or not message.content.startswith('!'): #Check if message is a command
        return

    # Get the command name from the message
    print(message.content)
    command_name = message.content[1:].split(' ')[0]  # strip the prefix and split

    # Check if the command exists in the collection
    command = client.Commands.get(command_name)

    if command:
        # Execute the command
        await command.execute(message, client)
    else:
        await message.channel.send('## [INFO]  \n**Command `'+command_name+'` not found.**')