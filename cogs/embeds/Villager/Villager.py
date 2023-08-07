import discord
import discord.colour

black = discord.colour.parse_hex_number('000000')

villager_role = discord.Embed(
    title="You are the Villager.",
    description="It's another normal day for good ol' villager. Just finished a day of hard work, and it's good to be back home. Hope nothing bad happens!",
    color=black
)
villager_role.add_field(
    name="What you do each night 🖐️",
    value="Nothing lol.",
    inline=True
)
villager_role.add_field(
    name="Visit type 🏃‍♂️",
    value="None",
    inline=True
)
villager_role.add_field(
    name="Side 👀",
    value="Villager",
    inline=True
)
villager_role.add_field(
    name="Goal 🥅",
    value="Help village win",
    inline=True
)
villager_role.add_field(
    name="Special Interactions ⭐",
    value=":white_small_square: None lol.",
    inline=True
)
villager_role.set_image(url='https://cdn.discordapp.com/attachments/1071466022395183164/1137757945652854896/villager.jpg')