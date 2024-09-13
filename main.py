# Imporant All Modules
import os
import importlib.util
import json
import discord
config = json.load(open('config.json'))

# Create Classes
class CommandCollection:
    def __init__(self):
        self.commands = {}

    def set(self, name, command):
        self.commands[name] = command

    def get(self, name):
        return self.commands.get(name)  
class EventCollection:
    def __init__(self, client):
        self.client = client

    def load_events(self):
        events_path = os.path.join(os.path.dirname(__file__), 'events')
        event_files = [f for f in os.listdir(events_path) if f.endswith('.py')]

        for file in event_files:
            file_path = os.path.join(events_path, file)
            spec = importlib.util.spec_from_file_location(file[:-3], file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'name') and hasattr(module, 'execute'):
                if getattr(module, 'once', False):
                    self.client.event(self.create_once_event(module.name, module.execute))
                else:
                    self.client.event(self.create_event(module.name, module.execute))
            else:
                print(f"[WARNING] The event at {file_path} is missing a required 'name' or 'execute' property.")

    def create_event(self, name, execute):
        async def event_handler(*args, **kwargs):
            await execute(self.client, *args, **kwargs)
        event_handler.__name__ = name
        return event_handler

    def create_once_event(self, name, execute):
        async def event_handler(*args, **kwargs):
            self.client.remove_listener(event_handler, name)
            await execute(self.client, *args, **kwargs)
        event_handler.__name__ = name
        return event_handler

#Make The Client Ready
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Create Collections
client.Commands = CommandCollection()
event_collection = EventCollection(client)

#Load Collections
event_collection.load_events() #Loads every Event in /events

folders_path = os.path.join(os.path.dirname(__file__), 'commands') #Get the path of the commands folder
command_folders = [f for f in os.listdir(folders_path) if os.path.isdir(os.path.join(folders_path, f))] #Get every folder in /commands

for folder in command_folders:
    commands_path = os.path.join(folders_path, folder) #Get path of the i folder in commands
    command_files = [f for f in os.listdir(commands_path) if f.endswith('.py')] #Get all files that end with .py
    for file in command_files:
        file_path = os.path.join(commands_path, file) #Get path of the file
        spec = importlib.util.spec_from_file_location(file[:-3], file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, 'data') and hasattr(module, 'execute'): #Check if the command file has 'data' and 'execute'
            client.Commands.set(module.data['name'], module) #Set the command in the collection
        else:
            print(f"[WARNING] The command at {file_path} is missing a required 'data' or 'execute' property.") #Warn if File misses 'data' or 'execute'


client.run(config['token'])