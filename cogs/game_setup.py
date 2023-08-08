import discord
from discord.ext import commands

from cogs.initialization import Join

class GameSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.setups_done = {}
        self.player_list = dict(zip(Join.players[0], Join.players[1]))

    async def create_mafia_game_channel(self, ctx):
        mafia_game_channel = await ctx.guild.create_text_channel('Ultimate_Mafia')
        mafia_role_thread = await mafia_game_channel.create_thread(name='Mafias', type=discord.ChannelType.private_thread)
        spectator_thread = await mafia_game_channel.create_thread(name='Spectators', type=discord.ChannelType.private_thread)
        return {'mafia_role_thread': mafia_role_thread, 'spectator_thread': spectator_thread}
    
    async def get_or_create_role(self, guild, role_name):
        #Helper function to get a role by name or create it if it doesn't exist
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
    async def setup(self, ctx):
        guild = ctx.guild
        role_name = "Mafia spectator"
        spectator_role = await self.get_or_create_role(guild, role_name)
        threads = await self.create_mafia_game_channel(ctx)
        self.bot.spectator_roles = {}    # Initialize the dictionary
        self.bot.spectator_roles[guild.id] = spectator_role
        mafia_role_thread = threads['mafia_role_thread']
        spectator_thread = threads['spectator_thread']

        self.setups_done[guild.id] = {'spectator_thread': spectator_thread, 'spectator_role': spectator_role}
        print(spectator_role) # prints out Mafia spectator
        print(self.setups_done)
        # assuming the spectator role exists in guild 
        await ctx.send("Press the button to join as spectator!", view=self.SpectatorView(spectator_role, self)) 
        # move the above to the future /start command as I want the spectator button shown then and as a ctx.send
    
    @commands.hybrid_command(name="spectator", description="Assigns spectator so you can watch Mafia 2.0 Games!")
    async def become_spectator(self, ctx):
        guild_id = ctx.guild.id
        if guild_id in self.setups_done:
            member = ctx.guild.get_member(ctx.author.id)
            players_class = self.bot.get_cog('Join')
            player_ids = players_class.players[1] if players_class else []

            if member.id not in player_ids:
                spectator_role = self.setups_done[guild_id]['spectator_role']
                print(self.setups_done[guild_id])
                print(spectator_role)
                await member.add_roles(spectator_role) # Command 'spectator' raised an exception: AttributeError: 'NoneType' object has no attribute 'id'
                await ctx.send("You are now a spectator!")
            else:
                await ctx.send('You are already a player!')
        else:
            await ctx.send('Setup has not been run for this guild!')
            


async def setup(bot):
    cog = GameSetup(bot)
    await bot.add_cog(cog)
