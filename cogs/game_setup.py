import discord
from discord.ext import commands

from cogs.initialization import Join
class GameSetup(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.setups_done = {}
        self.player_list = dict(zip(Join.players[0], Join.players[1]))

    class SpectatorButton(discord.ui.Button['SpectatorView']):
        def __init__(self, spectator_role: discord.Role):
            super().__init__(style=discord.ButtonStyle.green, label='Become a Spectator')
            self.spectator_role = spectator_role

        async def callback(self, interaction: discord.Interaction):
            member = interaction.user
            if self.spectator_role in member.roles or self.view.cog.player_list.get(member) != True:
                await interaction.response.send_message('You are already a spectator or not a player!', ephemeral=True)
            else:
                await member.add_roles(self.spectator_role)
                await interaction.response.send_message('You are now a spectator!', ephemeral=True)

    class SpectatorView(discord.ui.View):
        def __init__(self, spectator_role: discord.Role, cog):
            super().__init__()
            self.cog = cog
            self.add_item(GameSetup.SpectatorButton(spectator_role))

    @commands.hybrid_command(name="setup", description = "bot dev - temp for checking if channel creation works")
    async def setup(self, ctx):
        guild = ctx.guild
        spectator_role = discord.utils.get(guild.roles, name="spectator")
        # assuming the role exists in guild 
        mafia_game_channel = await guild.create_text_channel('Mafia 2.0')
        mafia_role_thread = await mafia_game_channel.create_thread(name='Mafias', type=discord.ChannelType.private_thread)
        spectator_thread = await mafia_game_channel.create_thread(name='Spectators', type=discord.ChannelType.private_thread)

        self.setups_done[guild.id] = {'spectator_thread': spectator_thread, 'spectator_role': spectator_role}

        #await spectator_thread.send("Press the button to join as spectator!", view=self.SpectatorView(spectator_role, self)) 
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