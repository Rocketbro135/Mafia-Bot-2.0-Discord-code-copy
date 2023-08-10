import discord
from discord.ext import commands
import discord.colour

# File imports
from cogs.Command_Settings.bot_settings import version, maxPartySize
from cogs.config import Gamemodes
import cogs.embeds.Villager.Villager
import cogs.embeds.Mafia.Reaper
import cogs.embeds.File_embeds.embeds as File_embeds


def get_current_gamemode(bot):
    cog = bot.get_cog('Gamemodes')
    if cog is not None:
        return cog.current_gamemode # gets current gamemode


class Join(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        #self.gamemodes_instance = gamemodes_instance

    players = ([], []) # author.name, author.id
    join_queue = [] # filled with author.id
    leave_queue = [] # filled with author.id

    @commands.hybrid_command(name='join', description = 'Joins the party in the server!')
    async def Join_Command(self, ctx):
        if len(Join.players[0]) == maxPartySize:
            # Adds the user's id into the join_queue list (later converts it to mention format)
            Join.join_queue.append(ctx.author.id)
            await ctx.send(embed=File_embeds.max_players_reached)

        else:
            # if the party is not full add user to the party
            Join.players[0].append(ctx.author.name)
            Join.players[1].append(ctx.author.id)

            joined_party_message = discord.Embed(
                title=ctx.author.name + " has joined the party.",
                description = "🥳Party Size: `" + str(len(Join.players[0])) + "`" + "\n🎲Current Mode: ",
                color=discord.colour.parse_hex_number('00FF00')
            )
            joined_party_message.add_field(
                name="",
                value=""
            )
            joined_party_message.set_footer(
                text="Current Patch: " + version + "\nType /party to see who's in the party!"
            )
            joined_party_message.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=joined_party_message)

    # Put leave command here
    @commands.hybrid_command(name="leave", description = "leave the mafia party...")
    async def Leave_Command(self, ctx):

        if(ctx.author.name not in Join.players[0]):
            await ctx.send(embed=File_embeds.not_in_party_embed)
            
        elif(ctx.author.name in Join.players[0]): # if game has not started leave the party
            Join.players[0].remove(ctx.author.name)
            Join.players[1].remove(ctx.author.id)

            leaveGameEmbed = discord.Embed(
                title="",
                description="",
                color=discord.Color.red()
            )
            leaveGameEmbed.add_field(
                name="",
                value=f"{ctx.author.name} left the party",
                inline=True
            )
            leaveGameEmbed.set_author(name="Mafiabot 2.0")

            await ctx.send(embed=leaveGameEmbed)

        #print("hello world")

    @commands.hybrid_command(name="queue", description = "See the current queue for the mafia party")
    async def Queue_Command(self, ctx):
        #print(Gamemodes.get_gamemode())
        print(get_current_gamemode(self.bot))
        #print(get_current_gamemode())
        #print(Gamemodes.get_current_gamemode())
        #print(gamemodes_instance.current_gamemode[0])
        #print(gamemodes_instance.get_current_gamemode())
        #print(gamemodes_instance.set_current_gamemode(gamemodes_instance.current_gamemode[0]))

        async def display_Join_Queue_Mentions():
            if not Join.join_queue:
                return "N/A"
            for id in Join.join_queue:
                mention = f'<@{id}>'
                return ":white_small_square:" + mention
            
        async def display_Leave_Queue_Mentions():
            if not Join.leave_queue:
                return "N/A"
            for id in Join.leave_queue:
                mention = f'<@{id}>'
                return ":white_small_square:" + mention

        embed = discord.Embed(
            title=":timer:" + str(ctx.guild) + " Queue",
            description="Players in join queue will automatically join the game once the current game finishes and those in leave queue will automatically leave.",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Join Queue",
            value=await display_Join_Queue_Mentions(),
            inline=True
        )
        embed.add_field(
            name="Leave Queue",
            value=await display_Leave_Queue_Mentions(), # I need to create leave queue as well
            #value=":white_small_square:" + str(Join.leave_queue), 
            inline=True
        )
        await ctx.send(embed=embed, allowed_mentions = False)

    @commands.hybrid_command(name="game", description = "Sends you a dm of how to play Mafia 2.0!")
    async def gameInfo_command(self, ctx):
        embed = discord.Embed(
            title="Info on the game has been sent to your dm!",
            description="",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

        gameInfoEmbed = discord.Embed(
            title="Mafia 2.0",
            description="At least 5 players, everyone must have Allow Direct Messages from Server Members ON in the Server's Privacy settings",
            color=discord.Color.orange()
        )
        gameInfoEmbed.add_field(
            name="1) Night time",
            value="Everyone goes to sleep. You will be prompted for your actions, each specific to your role",
            inline=False
        )
        gameInfoEmbed.add_field(
            name="2) Daytime",
            value="Visible actions that occured during Night time are revealed, everyone alive gets to discuss who the mafia is.",
            inline=False
        )
        gameInfoEmbed.add_field(
            name="3) Voting",
            value="The alive players will first nominate a person to the stand. The person on the stand will then be voted to whether be lynched or spared",
            inline=False
        )
        gameInfoEmbed.add_field(
            name="4) Repeat",
            value="Game continues until all threats to the town is eliminated or one side wins otherwise.",
            inline=False
        )
        gameInfoEmbed.set_footer(text="For more information, type /roles for roles, /help for commands.")
        gameInfoEmbed.set_image(url='https://dl.dropboxusercontent.com/scl/fi/jh1zp69y5lakj8nu0f0vm/Braum-Safe-Breaker-Fan-Art-Skin-By-Karamlik.png?dl=0&rlkey=e4rnqs9u6xo6vvbr5rzvf19sl')

        await ctx.author.send(embed=gameInfoEmbed)

    @commands.hybrid_command(name="party", description = "See who's in the party!")
    async def Party_command(self, ctx):
        async def display_Players():
            if not Join.players[0] or not Join.players[1]:
                return "N/A"
            players_list = [f":small_orange_diamond: {'Party leader:' if i == 0 else ''} <@{id}>" for i, id in enumerate(Join.players[1])]
            return "\n".join(players_list)
            
        async def display_Gamemodes():
            gamemodes = Gamemodes.Mafia_gamemodes() 
            return "\n".join([f"`{gamemode}` {'✅' if gamemode == get_current_gamemode(self.bot) else ''}" for gamemode in gamemodes])


        partyEmbed = discord.Embed(
            title=f":confetti_ball:`{ctx.guild.name}`:confetti_ball: Mafia Party",
            description=f":video_game:Current patch: `{version}`",
            color=discord.Color.purple()
        )
        partyEmbed.add_field(
            name=f"Players({len(Join.players[0])}) :man_detective:",
            value=await display_Players(),
            inline=True
        )
        partyEmbed.add_field(
            name="Current gamemode: :video_game:",
            value=await display_Gamemodes(),
            inline=True
        )

        partyEmbed.set_footer(text="When you're ready type /setup to start!")
        # partyEmbed.set # set the image here when when the bot pfp is made
        await ctx.send(embed=partyEmbed)

    @commands.hybrid_command(name="embedtester", description = "bot dev - temp for checking if embeds work")
    async def embedTester(self, ctx):
        await ctx.send(embed = cogs.embeds.Mafia.Reaper.reaper_role)

    @commands.hybrid_command(name="promote", description = "Promotes a member to party leader (Must be in party)")
    async def promote_command(self, ctx, user: discord.Member):
        # Check if Join.players[1] is not empty
        if Join.players[1]:
            # Check if the user to be promoted is already the party leader
            if user.id == Join.players[1][0]:
                await ctx.send(f"{user.display_name} is already the party leader.")
            else:
                # Check if the user to be promoted is in the party
                if user.id in Join.players[1]:
                    # Remove the user from the current position
                    user_index = Join.players[1].index(user.id)
                    Join.players[0].pop(user_index)
                    Join.players[1].pop(user_index)

                    # Put the user at the start of the list
                    Join.players[0].insert(0, user.name)
                    Join.players[1].insert(0, user.id)

                    await ctx.send(f"{user.mention} has been promoted to party leader.")
                else:
                    await ctx.send("The user you are trying to promote is not in the party.")
        else:
            await ctx.send("The party is currently empty.")

async def setup(bot):
    cog = Join(bot)
    await bot.add_cog(cog)
