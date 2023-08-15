import asyncio
import discord
from discord.ext import commands


class will_generation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.player_wills = {}

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
        # Sets the thumbnail url to the author's avatar profile picture
        updatedwill_embed.set_thumbnail(url=ctx.author.avatar.url)

        try:
            # Sends the embed to DM's
            await ctx.send(embed=updatedwill_embed)
        except discord.Forbidden:
                await ctx.send("It seems like I can't DM you. Please check your privacy settings.")

    @add_will_statement.error
    async def add_will_statement_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("You wouldn't want to leak your will would you! Do it in your DM's")


    @commands.dm_only()
    @commands.hybrid_command(name="erase", description = "Erase a line in your will!")
    async def remove_will_statement(self, ctx, *, index: int):
        player_id = ctx.author.id # Get the ID of the player who sent the command

        try:
            if player_id not in self.bot.player_wills: # checks if a will exists at the user's ID
                await ctx.send(f"{ctx.author.mention}, you haven't started your will yet! Type /write `insert words here` to start your will!")
            elif index <= 0 or index > len(self.bot.player_wills[player_id]): # checks the number of values in a container (lines) in player_wills[player_id]
                raise ValueError
        except ValueError:
            await ctx.send(f"{ctx.author.mention} ay yo, line {index} doesn't exist in your will. You currently have {len(self.bot.player_wills[player_id])} lines in your will.")
            return

        # Remove the will statement at the specified index
        removed_statement = self.bot.player_wills[player_id].pop(index-1)

        erasewill_embed = discord.Embed(
            title=f"Erased Line {index} of your Will ✍️",
            description=f"\"{removed_statement}\"",
            color=discord.Color.red()
        )

        # Create an embed to display the updated will
        updatedwill_embed = discord.Embed(
            title="✅ Your will has been updated.",
            color=discord.Color.green()
        )

        # Add each line of the will to the embed
        for i, line in enumerate(self.bot.player_wills[player_id], start=1):
            updatedwill_embed.add_field(name=f"Line {i}", value=line, inline=False)
        # Sets the thumbnail url to the author's avatar profile picture
        updatedwill_embed.set_thumbnail(url=ctx.author.avatar.url)

        try:
            # Sends the embeds to DM's
            await ctx.send(embed=erasewill_embed)
            await asyncio.sleep(1)
            await ctx.send(embed=updatedwill_embed)
        except commands.errors.PrivateMessageOnly:
            await ctx.send("It seems like I can't DM you. Please check your privacy settings.")

    @remove_will_statement.error
    async def add_will_statement_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("You wouldn't want to leak your will would you! Do it in your DM's")


    @commands.dm_only()
    @commands.hybrid_command(name="will", description = "Shows your will!")
    async def show_will(self, ctx):
        await ctx.defer()  # Sends a loading state to Discord (resolves the The application did not respond error)
        user_will = self.bot.player_wills.get(ctx.author.id) 
        if user_will:
            embed = discord.Embed(title="Your Will✍️", color=discord.Color.blue())
            for i, line in enumerate(user_will, start=1):
                embed.add_field(name=f"(Line {i})", value=line, inline=False)
            # Sets the thumbnail url to the author's avatar profile picture
            embed.set_thumbnail(url=ctx.author.avatar.url)

            # Send the users will
            try:
                await ctx.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("It seems like I can't DM you. Please check your privacy settings.")
        else:
            await ctx.send("You have not written a will yet.")

    @show_will.error
    async def show_will_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.send("You wouldn't want to leak your will would you! Do it in your DM's")

async def setup(bot):
    cog = will_generation(bot)
    await bot.add_cog(cog)
