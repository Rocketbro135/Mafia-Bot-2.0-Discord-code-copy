import discord
import discord.colour

black = discord.colour.parse_hex_number('000000')

doctor_role = discord.Embed(
    title="You are the Doctor.",
    description="As the village's only medical professional, the Doctor have all the knowledge in saving mafia victims. However, the online degree does not cover non-mafia victims.",
    color=black
)
doctor_role.add_field(
    name="What you do each night 🖐️",
    value="Visit a player and save them from the mafia.",
    inline=True
)
doctor_role.add_field(
    name="Visit type 🏃‍♂️",
    value="Active",
    inline=True
)
doctor_role.add_field(
    name="Side 👀",
    value="Villager",
    inline=True
)
doctor_role.add_field(
    name="Goal 🥅",
    value="Help villagers win",
    inline=True
)
doctor_role.add_field(
    name="Special Interactions ⭐",
    value=":white_small_square: You can only save targets from mafia attacks. :white_small_square:You cannot save the same person two nights in a row.",
    inline=True
)
doctor_role.set_image(url='https://cdn.discordapp.com/attachments/1102480259959509033/1138166603511496784/doctor.jpg')