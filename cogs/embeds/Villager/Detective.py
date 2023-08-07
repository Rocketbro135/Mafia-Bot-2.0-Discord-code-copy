import discord
import discord.colour

black = discord.colour.parse_hex_number('000000')

detective_role = discord.Embed(
    title="You are the Detective.",
    description="It is late at night. Another case was reported. It's time to start cracking the case and expose the mafias in this town...",
    color=black
)
detective_role.add_field(
    name="What you do each night 🖐️",
    value="Visit a player and learn if they belong to the mafia",
    inline=True
)
detective_role.add_field(
    name="Visit type 🏃‍♂️",
    value="Active",
    inline=True
)
detective_role.add_field(
    name="Side 👀",
    value="Villager",
    inline=True
)
detective_role.add_field(
    name="Goal 🥅",
    value="Help villagers win",
    inline=True
)
detective_role.add_field(
    name="Special Interactions ⭐",
    value=":white_small_square: If your target is framed by the framer, you will receive information that your target is mafia.",
    inline=True
)
detective_role.set_image(url='https://cdn.discordapp.com/attachments/1071466022395183164/1137764451970449569/detective.png')