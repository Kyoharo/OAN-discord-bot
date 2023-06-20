import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
activity = ["/", "OAN"]

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = commands.when_mentioned_or("!"),
            intents = discord.Intents.all(),
        )
    
    async def setup_hook(self): #overwriting a handler
        cogs_folder = f"{os.path.abspath(os.path.dirname(__file__))}/cogs"
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await client.tree.sync()
        print("Loaded cogs")

    
    async def on_ready(self):
        print(f"Bot connected as {self.user}")
        await self.change_presence(activity=discord.Game(random.choice(activity)))


client = Client()
@client.remove_command("help")
#---------------------------------------------         error CommandNotFound   -----------------------------------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore the error silently

    # Handle other types of errors if needed
    print(f"Error: {error}")


client.run(TOKEN)

