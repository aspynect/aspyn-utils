import discord
from discord import app_commands
import json
import random
import d20

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
with open('secrets.json', 'r') as file:
    secrets = json.load(file)

def sus(id):
    if id not in [439441145466978305, 99801098088370176]:
        return True
    return False

#TODO make an optional "visible" parameter on every command, default to ephemeral?

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="ping",description="ping")
async def ping(interaction: discord.Interaction):
    if sus(interaction.user.id):
        await interaction.response.send_message("impostor >:(", ephemeral = True)
        return
    await interaction.response.send_message("h", ephemeral = True)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="sync",description="sync")
async def sync(interaction: discord.Interaction):
    if sus(interaction.user.id):
        await interaction.response.send_message("impostor >:(", ephemeral = True)
        return
    await tree.sync()
    await interaction.response.send_message("sunk!", ephemeral = True)
    print("Sunk!")


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="uid",description="Send UID")
@app_commands.describe(game="Which UID?")
@app_commands.choices(game=[
        app_commands.Choice(name="Genshin", value="609006374"),
        app_commands.Choice(name="StarRail", value="604969370"),
        app_commands.Choice(name="Valorant", value="aspyn#sheit"),
        app_commands.Choice(name="Bungie", value="aspyn#5311")
    ])
        #TODO add switch fc
async def uid(interaction: discord.Interaction, game: app_commands.Choice[str]):
    if sus(interaction.user.id):
        await interaction.response.send_message("impostor >:(", ephemeral = True)
        return
    await interaction.response.send_message(game.value)
    


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="roll",description="Roll Dice!")
@app_commands.describe(dicestring="Dice Expression")
async def roll(interaction: discord.Interaction, dicestring: str):
    if sus(interaction.user.id):
        await interaction.response.send_message("impostor >:(", ephemeral = True)
        return
    try:
        result = str(d20.roll(dicestring))
    except: 
        await interaction.response.send_message("Invalid Expression", ephemeral = True)
        return
    await interaction.response.send_message(result)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="rollchar",description="Roll a Character!")
async def rollchar(interaction: discord.Interaction):
    if sus(interaction.user.id):
        await interaction.response.send_message("impostor >:(", ephemeral = True)
        return
    result = ""
    for i in range(6):
        result += f"{d20.roll("4d6rr1kh3")}\n"
    await interaction.response.send_message(result)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="rollhelp",description="Link to d20 docs")
async def rollhelp(interaction: discord.Interaction):
    if sus(interaction.user.id):
        await interaction.response.send_message("impostor >:(", ephemeral = True)
        return
    await interaction.response.send_message("https://github.com/avrae/d20?tab=readme-ov-file#operators", ephemeral = True)

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="ethics",description="Code of Ethics :3")
async def ethics(interaction: discord.Interaction):
    if sus(interaction.user.id):
        await interaction.response.send_message("impostor >:(", ephemeral = True)
        return
    ethicsArray = [
        "First of all, love the Lord God with your whole heart, your whole soul, and your whole strength.",
        "Then, love your neighbor as yourself.",
        "Do not murder.",
        "Do not commit adultery.",
        "Do not steal.",
        "Do not covet.",
        "Do not bear false witness.",
        "Honor all people.",
        "Do not do to another what you would not have done to yourself.",
        "Deny oneself in order to follow Christ.",
        "Chastise the body.",
        "Do not become attached to pleasures.",
        "Love fasting.",
        "Relieve the poor.",
        "Clothe the naked.",
        "Visit the sick.",
        "Bury the dead.",
        "Be a help in times of trouble.",
        "Console the sorrowing.",
        "Be a stranger to the world's ways.",
        "Prefer nothing more than the love of Christ.",
        "Do not give way to anger.",
        "Do not nurse a grudge.",
        "Do not entertain deceit in your heart.",
        "Do not give a false peace.",
        "Do not forsake charity.",
        "Do not swear, for fear of perjuring yourself.",
        "Utter only truth from heart and mouth.",
        "Do not return evil for evil.",
        "Do no wrong to anyone, and bear patiently wrongs done to yourself.",
        "Love your enemies.",
        "Do not curse those who curse you, but rather bless them.",
        "Bear persecution for justice's sake.",
        "Be not proud.",
        "Be not addicted to wine.",
        "Be not a great eater.",
        "Be not drowsy.",
        "Be not lazy.",
        "Be not a grumbler.",
        "Be not a detractor.",
        "Put your hope in God.",
        "Attribute to God, and not to self, whatever good you see in yourself.",
        "Recognize always that evil is your own doing, and to impute it to yourself.",
        "Fear the Day of Judgment.",
        "Be in dread of hell.",
        "Desire eternal life with all the passion of the spirit.",
        "Keep death daily before your eyes.",
        "Keep constant guard over the actions of your life.",
        "Know for certain that God sees you everywhere.",
        "When wrongful thoughts come into your heart, dash them against Christ immediately.",
        "Disclose wrongful thoughts to your spiritual mentor.",
        "Guard your tongue against evil and depraved speech.",
        "Do not love much talking.",
        "Speak no useless words or words that move to laughter.",
        "Do not love much or boisterous laughter.",
        "Listen willingly to holy reading.",
        "Devote yourself frequently to prayer.",
        "Daily in your prayers, with tears and sighs, confess your past sins to God, and amend them for the future."
        "Fulfill not the desires of the flesh; hate your own will.",
        "Obey in all things the commands of those whom God has placed in authority over you even though they (which God forbid) should act otherwise, mindful of the Lord's precept, 'Do what they say, but not what they do.'",
        "Do not wish to be called holy before one is holy; but first to be holy, that you may be truly so called.",
        "Fulfill God's commandments daily in your deeds.",
        "Love chastity.",
        "Hate no one.",
        "Be not jealous, nor harbor envy.",
        "Do not love quarreling.",
        "Shun arrogance.",
        "Respect your seniors.",
        "Love your juniors.",
        "Pray for your enemies in the love of Christ.",
        "Make peace with your adversary before the sun sets.",
        "Never despair of God's mercy."
    ]
    number = random.randint(0, len(ethicsArray) - 1)
    await interaction.response.send_message(f"{number + 1}: {ethicsArray[number - 1]}")

@client.event
async def on_ready():
    print("Ready!")

client.run(secrets["token"])