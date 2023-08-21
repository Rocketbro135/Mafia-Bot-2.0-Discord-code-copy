import typing
import discord
from discord.ext import commands
#import discord.colour

import cogs.Command_Settings.bot_settings as bot_settings

import cogs.embeds.File_embeds.embeds as File_embeds
import cogs.Command_Settings.bot_settings as Command_Settings

class Gamemodes(commands.Cog):
    # _instance = None possibly enable back if code breaks
    current_gamemode = None
    
    # def __new__(cls, bot: commands.Bot):
    #     if cls._instance is None:
    #         cls._instance = super(Gamemodes, cls).__new__(cls)
    #         # Put any initialization here.
    #         cls.current_gamemode = None
    #         return cls._instance
    
    # @classmethod
    # def set_gamemode(cls, gamemode):
    #     cls.current_gamemode = gamemode

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.current_gamemode: str | None
        #self.seconds = None
        self.get_seconds = None
        #_instance = None # possibly enable back if code breaks
        #current_gamemode = Gamemodes.get_gamemode()
    
    #def get_current_gamemode(self):
        #return self.current_gamemode[0]

    def Mafia_gamemodes():
        return ['Classic', 'Crazy', 'Chaos', 'Corona', 'Crimson']
    
    dmtime_min_seconds = 30
    dmtime_max_seconds = 120 # 2 minutes

    # min and max constants for talktime
    talktime_min_seconds = 30
    talktime_max_seconds = 120  # 2 minutes

    def set_seconds(self, seconds: int):
        self.seconds = seconds

    def get_seconds(self) -> int:
        # If self.seconds is None or less than 30, return 30, else return self.seconds 
        return max(self.seconds, Gamemodes.dmtime_min_seconds) if self.seconds is not None else Gamemodes.dmtime_min_seconds
        
    def set_talktime_seconds(self, seconds: int):
        """Sets the seconds for 'talktime' command."""
        self.talktime_seconds = seconds

    def get_talktime_seconds(self) -> int:
        """Returns max of 'talktime_seconds' or 'talktime_min_seconds' or 'talktime_min_seconds' if 'talktime_seconds' is None."""
        return max(self.talktime_seconds, Gamemodes.talktime_min_seconds) if self.talktime_seconds is not None else Gamemodes.talktime_min_seconds
    
    async def gamemode_autocomplete(
    self,
    ctx,
    current: str,
) -> typing.List[discord.app_commands.Choice[str]]:
        gamemodes = Gamemodes.Mafia_gamemodes()
        return [
            discord.app_commands.Choice(name=gamemode, value=gamemode) # the param that shows is mode
            for gamemode in gamemodes if current.lower() in gamemode.lower()
    ]

    async def talktime_seconds_autocomplete(
    self,
    ctx,
    current: str,
) -> discord.app_commands.Choice[str]:
        seconds = self.get_talktime_seconds()
        return discord.app_commands.Choice(name="seconds", value=seconds)
    
    async def seconds_autocomplete(
    self,
    ctx,
    current: str,
) -> discord.app_commands.Choice[str]:
        seconds = self.get_seconds()
        return discord.app_commands.Choice(name="seconds", value=seconds)

    # async def category_autocomplete(
    # self,
    # ctx,
    # current: str,
    # ) -> discord.app_commands.Choice[str]:

    # @classmethod
    # def get_gamemode(cls):
    #     return cls.current_gamemode

    @commands.hybrid_group(name='config')
    async def config(self, ctx):  
        pass
        
    @config.command(name="mode", description = "For gamemode options use /gamemode. If you are playing custom, use /custom cmode instead!")
    @discord.app_commands.autocomplete(gamemode=gamemode_autocomplete)
    async def mode(self, ctx, gamemode: str):
        if gamemode not in Gamemodes.Mafia_gamemodes():
            await ctx.send(embed=File_embeds.invalidEmbed)
        elif gamemode in Gamemodes.Mafia_gamemodes():
            server_name = ctx.guild.name
            server_id = ctx.guild.id
            successful_gamemode_set_embed = discord.Embed(
                title=f"✅Got it. {server_name} game mode has been set to {gamemode}! Have fun!",
                color=discord.Color.green()
            )
            # set the current gamemode here
            Gamemodes.current_gamemode = gamemode


            # be sure to add the following when a game is ongoing "You cannot change settings when a game is going on!"
            await ctx.send(embed=successful_gamemode_set_embed)
            return Gamemodes.current_gamemode
    
    @config.command(name='gamemode', description = 'See all possible games mode that you can play!', with_slash_command=True)
    async def view_gamemodes(self, ctx):
        # Sets the current gamemode in the footer
        if(Gamemodes.current_gamemode == None):
            File_embeds.avaliableGamemodes_Embed.set_footer(text="Current game mode: N/A")
        else:
            File_embeds.avaliableGamemodes_Embed.set_footer(text="Current game mode: " + Gamemodes.current_gamemode)

        await ctx.send(embed=File_embeds.avaliableGamemodes_Embed)

    @config.command(name="showdeadrole", description = "Toggle the showdeadrole setting! Decides whether a person's role is revealed after they die!")
    async def show_dead_role(self, ctx): # organize this later the database structure needs to be completed first
        server_id = ctx.guild.id
        dead_role_setting = bot_settings.dead_role_setting

        if(dead_role_setting == True):
            bot_settings.dead_role_setting = False
            await ctx.send(embed=File_embeds.disable_dead_role)
        else:
            bot_settings.dead_role_setting = True
            await ctx.send(embed=File_embeds.enable_dead_role)
        return dead_role_setting
    
    @config.command(name="dmtime", description = "The duration that the bots wait for your DM response at night!")
    @discord.app_commands.autocomplete(seconds=seconds_autocomplete)
    async def set_dm_time(self, ctx, seconds: int):
        Gamemodes.set_seconds(self.bot,seconds)
        print(Gamemodes.get_seconds(self.bot))
        dm_time_embed_equal = discord.Embed(
            title="Mafiabot 2.0",
            description=f"Got it. dmtime is now {seconds} seconds",
            color=discord.Color.red()
        )
        dm_time_embed_min = discord.Embed(
            title="Mafiabot 2.0",
            description=f"Sorry. The minimum time is {Gamemodes.dmtime_min_seconds} seconds.",
            color=discord.Color.red()
        )
        dm_time_embed_max = discord.Embed(
            title="Mafiabot 2.0",
            description=f"Sorry. The maximum time is {Gamemodes.dmtime_max_seconds} seconds.",
            color=discord.Color.red()
        )
        if seconds < Gamemodes.dmtime_min_seconds:
            await ctx.send(embed=dm_time_embed_min)
        elif seconds >= 120:
            await ctx.send(embed=dm_time_embed_max)
        else:
            Gamemodes.set_seconds(self.bot,seconds)
            dm_time_embed_equal = discord.Embed(
                title="Mafiabot 2.0",
                description=f"Got it. DM time is now {seconds} seconds",
                color=discord.Color.red()
            )

            await ctx.send(embed=dm_time_embed_equal)
            return seconds

    @config.command(name="talktime", description = "The duration for players to discuss during the day!")
    @discord.app_commands.autocomplete(seconds=talktime_seconds_autocomplete)
    async def set_talk_time(self, ctx, seconds: int):
        Gamemodes.set_talktime_seconds(self.bot,seconds)
        talk_time_embed_equal = discord.Embed(
            title="Mafiabot 2.0",
            description=f"Got it. Talk time is now {seconds} seconds",
            color=discord.Color.red()
        )
        talk_time_embed_min = discord.Embed(
            title="Mafiabot 2.0",
            description=f"Sorry. The minimum time is {Gamemodes.talktime_min_seconds} seconds.",
            color=discord.Color.red()
        )
        talk_time_embed_max = discord.Embed(
            title="Mafiabot 2.0",
            description=f"Sorry. The maximum time is {Gamemodes.talktime_max_seconds} seconds.",
            color=discord.Color.red()
        )
        if seconds < Gamemodes.talktime_min_seconds:
            await ctx.send(embed=talk_time_embed_min)
        elif seconds >= Gamemodes.talktime_max_seconds:
            await ctx.send(embed=talk_time_embed_max)
        else:
            await ctx.send(embed=talk_time_embed_equal)
            return seconds

    @config.command(name="category", description = "Set the category that the bot creates the text channel in!") 
    async def set_channel(self, ctx, category: discord.CategoryChannel):
        if not hasattr(self.bot, 'category_channels'):
            self.bot.category_channels = {}
        
        self.bot.category_channels[ctx.guild.id] = category.id
        # category_id = self.bot.category_channels.get(guild.id, None) In order to access it in other channels use the following
        setup_game_embed = discord.Embed(
            title="Mafiabot 2.0",
            description=f"Got it. I will now create text channels at #{category} from now on.",
            color=discord.Colour.red()
        )
        
        setup_game_embed.set_thumbnail(url=Command_Settings.bot_image_thumbnail_url)        
        await ctx.send(embed=setup_game_embed)

    @commands.hybrid_command(name="setting", description = "Shows the current setting for this server!")
    async def show_setting(self, ctx):
        current_settings_embed = discord.Embed(
            title=f"Current settings on {ctx.guild.name}",
            description="Customizable settings for Mafiabot 2.0",
            color=discord.Color.og_blurple()
        )
        current_settings_embed.add_field(
            name="gamemode",
            value=Gamemodes.current_gamemode,
            inline=True
        )
        current_settings_embed.add_field(
            name="dmtime",
            value=Gamemodes.get_seconds(self.bot),
            inline=True
        )

        await ctx.send("working on the command now")
        await ctx.send(embed=current_settings_embed)

#spectator_roles = self.bot.spectator_roles
#print(spectator_roles)

async def setup(bot):
    cog = Gamemodes(bot)
    await bot.add_cog(cog)
