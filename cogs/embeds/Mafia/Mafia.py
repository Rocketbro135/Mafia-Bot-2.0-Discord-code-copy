import discord
import discord.colour

black = discord.colour.parse_hex_number('000000')

mafia_role = discord.Embed(
    title="You are the Mafia.",
    description="The Godfather's right hand. The mafia lives to serve the Godfather, doing the biddings the Godfather commands. That is always how it is... for now...",
    color=black
)
mafia_role.add_field(
    name="What you do each night 🖐️",
    value="Kill the target the Godfather chooses.",
    inline=True
)
mafia_role.add_field(
    name="Visit type 🏃‍♂️",
    value="Active",
    inline=True
)
mafia_role.add_field(
    name="Side 👀",
    value="Mafia",
    inline=True
)
mafia_role.add_field(
    name="Goal 🥅",
    value="Help mafias win",
    inline=True
)
mafia_role.add_field(
    name="Special Interactions ⭐",
    value=":white_small_square: If the Godfather dies, you may become the next Godfather.",
    inline=True
)
mafia_role.set_image(url='https://cdn.discordapp.com/attachments/1102480259959509033/1138166709241520220/mafia.png')
