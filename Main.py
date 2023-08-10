import os
from typing import Literal, Optional
import discord
from dotenv import load_dotenv
from discord.ext import commands

#from cogs.gamemodes import Gamemodes
#from cogs.gamemodes import gamemodes_instance

load_dotenv('Discord_Token.env')
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix= 'Mafia.', intents = intents)

class MyBot(commands.Bot):
    #bot.command_prefix
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        print("Bot is starting...")
        await self.load_extension('cogs.initialization')
        await self.load_extension('cogs.config')
        await self.load_extension('cogs.wills')
        await self.load_extension('cogs.game_setup')

bot = MyBot(command_prefix=bot.command_prefix, intents=bot.intents)
#cog = bot.get_cog("Gamemodes")
#gamemodes_instance = Gamemodes(bot)
#gamemodes_instance.set_bot(bot)



# category = ""
# @bot.tree.command(name="selects from the available categories")
# async def testing(ctx, category: discord.CategoryChannel):
#     string = f"{category}"
#     await ctx.send(string)


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")



@bot.event
async def on_ready():
    print("Bot is online")
    print(bot.get_guild(1063247287561765005))

bot.run(TOKEN)
