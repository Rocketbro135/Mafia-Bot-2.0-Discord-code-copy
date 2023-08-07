import discord

invalidEmbed = discord.Embed(
                title="Error: Invalid game mode.\ntype /gamemodes to view all available game modes!",
                color=discord.Color.red()
            )
invalidEmbed.add_field(
                name="",
                value="(If you're trying to set a premium mode, you have to join the party first.)",
                inline=False
            )

avaliableGamemodes_Embed = discord.Embed(
            title="Avaliable Game Modes!",
            description="To set a gamemode, type /config mode `mode`",
            color=discord.Color.blue()
            )
avaliableGamemodes_Embed.add_field(
            name="Classic:grinning::champagne_glass: (/config mode classic)",
            value="The classic mafia you play with friends! Recommended for small parties.",
            inline=False
            )
avaliableGamemodes_Embed.add_field(
            name="Crazy:grimacing::dagger: (/config mode crazy)",
            value="Fun roles to spice up your boring classic games! Recommended for medium size parties(>6).",
            inline=False
            )
avaliableGamemodes_Embed.add_field(
            name="Chaos:smiling_imp::fire: (/config mode chaos)",
            value="Absolute chaos where lots of neutral roles could be in play. Recommended for big parties(>9).",
            inline=False
            )
avaliableGamemodes_Embed.add_field(
            name="Corona🤒🧻 (/config mode corona)",
            value="Even more chaotic roles that lives up to its name. Recommended for big parties(>9).",
            inline=False
            )
avaliableGamemodes_Embed.add_field(
            name="Crimson🩸🔪 (/config mode crimson)",
            value="Filled with mysterious roles, you'll have no idea what could happen next!",
            inline=False
            )
avaliableGamemodes_Embed.set_image(url='https://cdna.artstation.com/p/assets/images/images/008/842/476/original/atey-ghailan-progress-gif.gif?1515633758')

enable_dead_role = discord.Embed(
            title="Showdeadrole has turned on!",
            description="",
            color=discord.Color.green()
            )
enable_dead_role.add_field(
            name="",
            value="✅💀This means when someone dies, their role will be revealed to everyone!\n🚫📜This also means wills are NOT in play!",
            inline=True
            )

disable_dead_role = discord.Embed(
            title="Showdeadrole has turned off!",
            description="",
            color=discord.Color.red()
            )
disable_dead_role.add_field(
            name="",
            value="🚫💀This means when someone dies, their role will NOT be revealed to everyone!\n✅📜This also means wills are in play!",
            inline=True
            )