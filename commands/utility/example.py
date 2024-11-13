data = { ##Set The Commands Data
    "name":"example", ##Set the Name of the Command
    "description":"Example Command" ##Set the Command's description
}
async def execute(message, client): ##Handle the execution of the Command
    await message.channel.send('Example Command Execute') ##Send an Answer, Use the discord.py Docs to find out more 
