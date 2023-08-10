import discord
from discord.ext import commands


class will_generation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.player_wills = {}

    # show_will = discord.Embed(
    #     title="Your will ✍️",
    #     description="",
    #     color=discord.Color.green()
    # )

    @commands.dm_only()
    @commands.hybrid_command(name="write", description = "Write a line to your will here!") #potentially add a limit for the amount off will statements?
    async def add_will_statement(self, ctx, *, will_statement): # the * is there to take in spaces in the will_statement
        guild = ctx.guild 
        player_id = ctx.author.id # Get the ID of the player who sent the command

        # If the player doesn't have a will yet, create a new one
        if player_id not in self.bot.player_wills:
            self.bot.player_wills[player_id] = [] # Creates will based on player_id
            # Potentially create the will based on player_id and guild.id
        
        # Add the new will statement to the player's will
        self.bot.player_wills[player_id].append(will_statement)

        # Create an embed to display the updated will
        updatedwill_embed = discord.Embed(
            title="✅ Your will has been updated.",
            color=discord.Color.green()
        )

        # Add each line of the will to the embed
        for i, line in enumerate(self.bot.player_wills[player_id], start=1):
            updatedwill_embed.add_field(name=f"Line {i}", value=line, inline=False)

        # Send the embed to the channel
        await ctx.send(embed=updatedwill_embed)

    @add_will_statement.error
    async def add_will_statement_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("You wouldn't want to leak your will would you! Do it in your DM's")

    # Command can be used in both server channel and DM, it will send in DM's however.
    @commands.hybrid_command(name="will", description = "Shows your will!")
    async def show_will(self, ctx):
        user_will = self.bot.player_wills.get(ctx.author.id) 
        if user_will:
            embed = discord.Embed(title="Your Will✍️", color=discord.Color.blue())
            for i, line in enumerate(user_will, start=1):
                embed.add_field(name=f"(Line {i})", value=line, inline=False)
            # Sets the thumbnail url to the author's avatar profile picture
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.author.send(embed=embed)
        else:
            await ctx.author.send("You have not written a will yet.")


async def setup(bot):
    cog = will_generation(bot)
    await bot.add_cog(cog)
