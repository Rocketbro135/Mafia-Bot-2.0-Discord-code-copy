import discord
import discord.colour

black = discord.colour.parse_hex_number('000000')

godfather_role = discord.Embed(
    title="You are the Godfather.",
    description="Godfather is the big bad boss of the town. Every mafia is under his thumb, ready to execute the Godfather's will.",
    color=black
)
godfather_role.add_field(
    name="What you do each night 🖐️",
    value="If a mafia is alive, order the mafia to kill a target of your choosing. If no mafias are alive, you kill the target yourself.",
    inline=True
)
godfather_role.add_field(
    name="Visit type 🏃‍♂️",
    value="Passive/Active",
    inline=True
)
godfather_role.add_field(
    name="Side 👀",
    value="Mafia",
    inline=True
)
godfather_role.add_field(
    name="Goal 🥅",
    value="Help mafias win",
    inline=True
)
godfather_role.add_field(
    name="Special Interactions ⭐",
    value=":white_small_square:If you die, one of your mafias alive will become the new Godfather. :white_small_square:If you order a mafia to kill, you will not visit anyone.",
    inline=True
)
godfather_role.set_image(url='https://cdn.discordapp.com/attachments/1102480259959509033/1138167550652457071/godfather.jpg')
