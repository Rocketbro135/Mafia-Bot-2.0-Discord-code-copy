from test1 import my_object
from cogs.config import Gamemodes
from Main import test

print(my_object.my_attribute)

# Suppose that you have a Bot instance named 'bot'
bot_instance = Gamemodes  # replace 'bot' with your actual discord.Bot instance

# Get instance of Gamemodes class
gamemode_instance = Gamemodes(bot_instance)

# Print the current gamemode
print(gamemode_instance.get_gamemode())
print(test)