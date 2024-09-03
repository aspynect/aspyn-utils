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
#TODO unit conversions (ephemeral)

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
        app_commands.Choice(name="Steam", value="883076786"),
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
@tree.command(name="temperature",description="Convert Temperatures")
@app_commands.describe(input="Input amount and units (with a space)")
async def roll(interaction: discord.Interaction, input: str):
    if sus(interaction.user.id):
        await interaction.response.send_message("impostor >:(", ephemeral = True)
        return
    
    input.lower()
    inputArray = input.split()
    tempNum = float(inputArray[0])
    tempUnit = inputArray[1]
    if len(inputArray) < 2:
        await interaction.response.send_message("Invalid Input! No spaces!", ephemeral = True)
    tempInF = 0
    match tempUnit:
        case "f":
            tempInF = tempNum
        case "c":
            tempInF = tempNum * 1.8 + 32
        case _:
            await interaction.response.send_message("Invalid Unit", ephemeral = True)
            return
    outputString = ""
    outputString += f"{tempInF:.1f} Degrees Fahrenheit\n"
    outputString += f"{(tempInF - 32) / 1.8:.1f} Degrees Celsius\n"
    await interaction.response.send_message(outputString, ephemeral = True)


    #await interaction.response.send_message(result)

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
    await interaction.response.send_message(f"{number + 1}. {ethicsArray[number]}")


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="advice",description="Advice for Budding Streamers")
async def advice(interaction: discord.Interaction):
    if sus(interaction.user.id):
        await interaction.response.send_message("impostor >:(", ephemeral = True)
        return
    adviceArray = [
        "1. Be kind and wholesome; positivity is inherently contagious.",
        "2. Be yourself, but be measured: people want authenticity, but too much feels like therapy.",
        "3. Model the behavior you want to see in your followers.",
        "4. Have an extremely cool penis.",
        "5. Be famous, sexually-active, and have a large social media following.",
        "6. Be very famous, have a huge social media following, and be extremely sexually-active.",
        "7. Dig up a skeleton from the cemetery on stream.",
        "8. Find a sick child and film him. Viewers appreciate sick children.",
        "9. Give your dog a math problem and stream him struggling with it. Viewers like to know they're not alone.",
        "10. Add a laugh track to your stream so that your audience knows when to laugh. This will help remind your audience that they have missed out on a golden opportunity to laugh.",
        "11.  Never make your streaming schedule too rigid. You want to give yourself an opportunity to take a day off.",
        "12. Film the future. It will give your viewers on opportunity to make trades from which they can profit handsomely.",
        "13. Relish the opportunity to correct your own misstatements. It's not a sign of weakness: it gives viewers comfort to know that you're fallible too.",
        "14. Show your iPad screen when you're playing a mobile game: people love to know that their heroes have iPads.",
        "15. Let your viewers know that you're (eventually) going to tell them how to get rich off of bitcoin; but to shut the fuck, be quiet, and focus on your stream until you're ready to tell them.",
        "16. Charge your phone on camera (optional).",
        "17. The best streamers are even better listeners. Your followers didn't show up to listen to you talk all day — they showed up to listen to you listen.",
        "18. Bend your viewers to your will.",
        "19. Never forget your roots. Your stream started out on Justin.tv, which was a platform designed for traditional content distribution. Give a shout out to Justin every once in a while.",
        "20. Require that users enable Macromedia Flash Player to view your stream.",
        "21. Share some of your passwords with your audience to establish trust.",
        "22. You don't have to stream games! Sometimes your viewers just want a crash course on how to build a nuclear bomb, or a history lesson on Syrian military victories.",
        "23. Don't be afraid to give your viewers a reason to fear and hate you.",
        "24. Play Russian Roulette on stream. Tell your viewers that you'll add a bullet to the chamber for every donation.",
        "25. Donate to yourself on stream to show to your audience that you're just as invested in your own success as they are.",
        "26. Followers remember what they see, and they'll forget the things they never saw.",
        "27. When it's hot out, make sure to drink water on stream. When it's cold out, make sure to drink hot chocolate. Be consistent.",
        "28. Don't be afraid to show your belly button and/or asshole.",
        "29. People who chat the most, donate the least. Eliminate them.",
        "30. Tell your viewers to hold their applause until the end. Ban anybody who doesn't listen.",
        "31. Constantly remind your viewers that 'age is just a number.'",
        "32. Release your complete tax returns and long-form birth certificate on stream so the audience knows you're a red-blooded American."
    ]
    number = random.randint(0, len(adviceArray) - 1)
    await interaction.response.send_message(f"{adviceArray[number]}")

@client.event
async def on_ready():
    print("Ready!")

client.run(secrets["token"])