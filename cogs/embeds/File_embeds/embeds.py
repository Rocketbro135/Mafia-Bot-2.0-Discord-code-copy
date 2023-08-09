import discord
from cogs.Command_Settings.bot_settings import bot_image_thumbnail_url as thumbnail_image

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

max_players_reached = discord.Embed(
            title="",
            description="The max amount of players is reached! Type /queue to see the queue.",
            color=discord.colour.parse_hex_number('FF0000')
            )
max_players_reached.set_author(
            name="Mafiabot 2.0",
            icon_url= "https://cdn.wanderer.moe/honkai-star-rail/splash-art/yanqing-full.png"
            )

not_in_party_embed = discord.Embed(
                title="",
                description="",
                color=discord.Color.red()
            )
not_in_party_embed.add_field(
                name="",
                value="You are not in the party lol😅",
                inline=True
            )
not_in_party_embed.set_author(name="Mafiabot 2.0")

setup_game_embed = discord.Embed(
    title="Everything's ready! Everyone feel free to join a voice chat and /start to start the game!",
    description=" Make sure you understand how the game works! (Info can be found with /game)",
    color=discord.Color.green()
)
setup_game_embed.set_thumbnail(url='https://pbs.twimg.com/media/DWVbyz5WsAA93-y.png')

start_game_embed_Fail = discord.Embed(
    title="",
    description="You didn't set up yet. Type /setup first.",
    color=discord.Color.red()
)
start_game_embed_Fail.set_thumbnail(url=thumbnail_image)
