from nextcord.ext import commands
from cog import Cog
from dotenv import load_dotenv
from os import getenv

prefix = '%'
bot = commands.Bot(command_prefix=prefix)
bot.add_cog(Cog(bot))

load_dotenv()
token = getenv('TOKEN')

bot.run(token)

