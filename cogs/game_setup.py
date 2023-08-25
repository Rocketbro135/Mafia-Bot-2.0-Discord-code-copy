import asyncio
import discord
from discord.ext import commands

from cogs.initialization import Join
import cogs.embeds.File_embeds.embeds as File_embeds
#from cogs.config import Gamemodes

# def get_current_gamemode(bot):
#     cog = bot.get_cog('Gamemodes')
#     if cog is not None:
#         return cog.current_gamemode # gets current gamemode


class GameSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.setups_done = {}
        self.player_list = {}

    async def initialize_player_list(self): # add an except error later where a message shows if a user tries to setup a game before joining in the guild
        join_cog = self.bot.get_cog('Join')
        if join_cog:
            print(join_cog.players)
            player_data = list(join_cog.players.values())[0]
            self.player_list = dict(zip(player_data['names'], player_data['ids']))

    async def create_mafia_game_channel(self, ctx, role_name, category_id):
        guild = ctx.guild
        await self.initialize_player_list()
        #join_cog = self.bot.get_cog('Join')
        category = guild.get_channel(category_id)
        spectator_role = await self.get_or_create_role(guild, role_name)

        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True) # guild.me is the bot itself
        }

        default_overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True) # guild.me is the bot itself
        }

        # Gets the players currently Joined and puts their id's in joined_player_ids
        #joined_player_ids = [guild.get_member(player_id) for player_id in join_cog.players[1] if guild.get_member(player_id) is not None]
        joined_player_ids = [guild.get_member(player_id) for player_id in self.player_list.values() if guild.get_member(player_id) is not None]

        for joined_player in joined_player_ids:
            overwrites[joined_player] = discord.PermissionOverwrite(read_messages=True, send_messages=False)

        # Creating the Game channel & Setting permissions for spectator role. Makes the Mafia_Team thread
        # Threads share permissions with the parent channel; position 0 is the top of the category
        mafia_game_channel = await category.create_text_channel(name='Ultimate_Mafia', overwrites=overwrites, position=0)
        await mafia_game_channel.set_permissions(spectator_role, view_channel=True, send_messages=False)
        mafia_role_thread = await mafia_game_channel.create_thread(name='Mafias', type=discord.ChannelType.private_thread)

        # Creating the Spectator channel & Setting permissions for spectator role.
        spectator_channel = await category.create_text_channel(name='Spectators', overwrites=default_overwrites, position=1)
        await spectator_channel.set_permissions(spectator_role, view_channel=True, send_messages=True)

        print(mafia_role_thread)
        print("---")
        print(mafia_game_channel)
        print("---")
        print(spectator_role)

        #spectator_thread = await mafia_game_channel.create_thread(name='Spectators', type=discord.ChannelType.private_thread)
        return {'mafia_role_thread': mafia_role_thread, 'spectator_channel': spectator_channel, 'mafia_game_channel': mafia_game_channel}
    
    async def get_or_create_role(self, guild, role_name):
        # Helper function to get a role by name or create it if it doesn't exist
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            permissions = discord.Permissions(send_messages=True, read_messages=True)  # Example: Adjust as needed
            role = await guild.create_role(name=role_name, permissions=permissions)
        return role

    class SpectatorButton(discord.ui.Button['SpectatorView']):
        def __init__(self, spectator_role: discord.Role):
            super().__init__(style=discord.ButtonStyle.green, label='Become a Spectator')
            self.spectator_role = spectator_role

        async def callback(self, interaction: discord.Interaction):
            member = interaction.user
            if self.spectator_role in member.roles:
                await interaction.response.send_message('You are already a spectator!', ephemeral=True)
            elif self.view.cog.player_list.get(member): 
                await interaction.response.send_message('You are already participating in the game as a player!', ephemeral=True)
            else:
                try:
                    await member.add_roles(self.spectator_role)
                    await interaction.response.send_message('You are now a spectator!', ephemeral=True)
                except Exception as e:
                    await interaction.response.send_message(f'An error occured: {str(e)}', ephemeral=True)

    class SpectatorView(discord.ui.View):
        def __init__(self, spectator_role: discord.Role, cog):
            super().__init__()
            self.cog = cog
            self.add_item(GameSetup.SpectatorButton(spectator_role))

    @commands.hybrid_command(name="setup", description = "bot dev - temp for checking if channel creation works")
    async def setup(self, ctx): # ensure that config settings are made before the command runs
        guild = ctx.guild
        gamemode = self.bot.get_cog('Gamemodes').get_current_gamemode(guild.id)

        if gamemode == None:
            await ctx.send("Please select a gamemode with /gamemode")
        else:

            role_name = "Mafia spectator"
            spectator_role = await self.get_or_create_role(guild, role_name)

            # Tries to get the category channel from the bot's stored category_channels if not creates id at current location
            try:
                #self.bot.category_channels:
                category_id = self.bot.category_channels.get(guild.id)
            except:
                category_id = ctx.channel.category_id
            
            print(category_id)

            # Create the channels in the specified category, or in the guild if no category is specified
            if category_id:
                threads = await self.create_mafia_game_channel(ctx, role_name, category_id)
            else:
                category_id = ctx.channel.category.id
                threads = await self.create_mafia_game_channel(ctx, category_id)

            self.bot.spectator_roles = {}    # Initialize the dictionary
            self.bot.spectator_roles[guild.id] = spectator_role
            mafia_role_thread = threads['mafia_role_thread']
            mafia_game_channel = threads['mafia_game_channel']
            spectator_channel = threads['spectator_channel']

            self.setups_done[guild.id] = {
                'spectator_channel': spectator_channel,
                'spectator_role': spectator_role,
                'mafia_role_thread': mafia_role_thread,
                'mafia_game_channel': mafia_game_channel
            }

            print(spectator_role) # prints out Mafia spectator
            print(self.setups_done)


            # developing the random generation of roles that players will get in mafia
            
            # develop code so that it requires a gamemode to be set (done)

            #await ctx.send("Press the button to join as spectator!", view=self.SpectatorView(spectator_role, self)) 
            # move the above to the future /start command as I want the spectator button shown then and as a ctx.send (done)
            await ctx.send(embed=File_embeds.setup_game_embed)
    
    @commands.hybrid_command(name="start", description = "Start the mafia game with all current party members!") # reminder to move config channel command to other file
    async def start_game_command(self, ctx):
        guild_id = ctx.guild.id
        gamemode = self.bot.get_cog('Gamemodes').get_current_gamemode(guild_id)

        # Check if the setup has been done
        if guild_id in self.setups_done:
            # Check if the user is the party leader
            join_cog = self.bot.get_cog('Join')
            if join_cog and join_cog.players[guild_id]['ids'] and ctx.author.id == join_cog.players[guild_id]['ids'][0]:
                spectator_role = self.setups_done[guild_id]['spectator_role']
                await ctx.send("Press the button to join as spectator!", view=self.SpectatorView(spectator_role, self))

                # Mentioning all users in the Ultimate_Mafia channel
                guild = ctx.guild
                mafia_game_channel = discord.utils.get(guild.text_channels, id=self.setups_done[guild.id]['mafia_game_channel'].id)
                if mafia_game_channel:
                    print(join_cog.players[guild_id]['ids'])
                    players_mention = " ".join([f"<@{player}>" for player in join_cog.players[guild_id]['ids']])
                    await mafia_game_channel.send(f"{players_mention}") # mafia_game_channel.send(f"Attention all players: {players_mention}, the game is about to start!")
                    await mafia_game_channel.send(embed=File_embeds.welcome_to_mafia_embed)
                    await asyncio.sleep(3) # Wait before sending the next embed
                    await mafia_game_channel.send(embed=File_embeds.will_system_embed) 

                    # develop code to where users will be pinged in the mafia channel (done)
                    # there roles need to be chosen beforehand
                    # users in the party will need to be 

                start_game_embed_Success = discord.Embed(
                    title="",
                    description=f"Please wait. Setting game with mode: {gamemode}",
                    color=discord.Color.red()
                )

                await ctx.send(embed=start_game_embed_Success)  # make sure to add the other embed for starting the game
            else:
                await ctx.send('You are not the party leader!')
        else:
            await ctx.send('Setup has not been run for this guild!')

    @commands.hybrid_command(name="spectator", description = "Assigns spectator so you can watch Mafia 2.0 Games!")
    async def become_spectator(self, ctx):
        guild_id = ctx.guild.id
        join_cog = self.bot.get_cog('Join')

        if guild_id in self.setups_done:
            member = ctx.guild.get_member(ctx.author.id)

            if member is None:
                await ctx.send('You are not a member!')
                return
            
            if join_cog and member.id in join_cog.players[guild_id]['ids']:
                await ctx.send('You are already a player!')
                return
            
            spectator_role = self.setups_done[guild_id]['spectator_role']
        
            if spectator_role is None:
                await ctx.send('No spectator role found!')
                return
        
            await member.add_roles(spectator_role)
            await ctx.send("You are now a spectator!")
        else:
            await ctx.send('Setup has not been run for this guild!')
                

async def setup(bot):
    cog = GameSetup(bot)
    await bot.add_cog(cog)
