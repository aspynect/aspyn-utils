import discord
from discord import app_commands
import json
import random
import d20
import requests
from io import BytesIO
from os import path
from subprocess import run, PIPE
import magic


myColor = discord.Color.from_rgb(r=255, g=0, b=255)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
with open('secrets.json', 'r') as file:
    secrets = json.load(file)
headmatesList = ["aspyn", "Cassie", "Shane", "Ruth", "nea", "Pearl"]

class Anime():
    def __init__(self):
        self.animeInfo = self.getAnimeList()
    
    def getAnimeList(self):
        response = requests.get("https://api.myanimelist.net/v2/users/aspynect/animelist?status=completed&sort=list_score&limit=25&fields=id,title,mean,main_picture,list_status,alternative_titles", headers = {'X-MAL-CLIENT-ID': secrets["mal-token"]})
        response.raise_for_status()
        anime_list = response.json()
        response.close()
        animeList = anime_list['data']
        optionsList = []
        for index in range(len(animeList)):
            anime = animeList[index]["node"]
            optionsList.append(discord.SelectOption(label = anime['title'], value = index, description = anime['alternative_titles']['en']))
        return [animeList, optionsList]

    def embed(self, anime):
        animeNode = anime["node"]
        embed = discord.Embed(title = animeNode["title"], description = animeNode["alternative_titles"]["en"], color = myColor, url = f"https://myanimelist.net/anime/{animeNode['id']}")
        embed.add_field(name = "Mean Rating", value = animeNode["mean"])
        embed.add_field(name = "My Rating", value = anime["list_status"]["score"])
        embed.set_image(url = animeNode["main_picture"]["large"])
        return embed
    
    def embedTwo(self, index):
        anime = self.getAnime(index)
        return self.embed(anime)
    
    def getAnime(self, index):
        anime = self.animeInfo[0][int(index)]
        return anime


async def sus(id):
    if id not in [439441145466978305, 99801098088370176]:
        return True
    return False

async def vote(interaction: discord.Interaction):
        embed = discord.Embed(title = "impostor >:(", color = discord.Color.red())
        embed.set_image(url="attachment://sus.webp")
        await interaction.response.send_message(embed = embed, ephemeral = True, file = discord.File('assets/sus.webp'))
        await snitch(interaction)


async def snitch(interaction: discord.Interaction):
    aspynUser = await client.fetch_user(439441145466978305)
    embed = discord.Embed(title = "Impostor Alert", color = myColor)
    embed.add_field(name = "Name", value = interaction.user.display_name)
    embed.add_field(name = "user", value = interaction.user.name)
    embed.add_field(name = "Command", value = interaction.command.name)
    embed.add_field(name = "ID", value = interaction.user.id)
    embed.add_field(name = "Mention", value = f"<@{interaction.user.id}>")
    embed.set_image(url = interaction.user.avatar.url)
    await aspynUser.send(embed = embed)

#TODO currency conversions (ephemeral)
#TODO doesthedogdie?

animeThings = Anime()
class AnimeSelector(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.select(placeholder = "Select an anime", options = animeThings.animeInfo[1], max_values=1)
    async def animeSelector(self, interaction: discord.Interaction, select: discord.ui.Select):
        anime = select.values[0]
        embed = animeThings.embedTwo(anime)
        await interaction.response.edit_message(embed = embed)


class CounterButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.counter = 0

    @discord.ui.button(label = "- 1")
    async def subButton(self, interaction: discord.Interaction, button:discord.ui.Button):
        self.counter -= 1
        await interaction.response.edit_message(content = self.counter)

    @discord.ui.button(label = "+ 1")
    async def addButton(self, interaction: discord.Interaction, button:discord.ui.Button):
        self.counter += 1
        await interaction.response.edit_message(content = self.counter)


class SystemViews(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.imageIndex = 0
        with open('system.json', 'r') as file:
            self.infoDict = json.load(file)
        self.currentMember = ""

    async def buildAndSend(self, interaction: discord.Interaction):
        member = self.infoDict[self.currentMember]
        embed = discord.Embed(color = myColor, title = f"{self.currentMember} • {member["pronouns"]}")
        embed.description = member["bio"]
        embed.set_image(url = "attachment://image.webp")
        embed.set_footer(text = f"Image {self.imageIndex + 1}/{len(member["images"])}")
        await interaction.response.edit_message(embed = embed, attachments = [discord.File(member["images"][self.imageIndex], filename = "image.webp")])

    @discord.ui.select(placeholder = "Select a headmate", options = [discord.SelectOption(label = headmatesList[i], value = i) for i in range(len(headmatesList))], max_values=1)
    async def headmateSelector(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.imageIndex = 0
        self.currentMember = headmatesList[int(select.values[0])]
        await self.buildAndSend(interaction)

    @discord.ui.button(label = "←")
    async def prevButton(self, interaction: discord.Interaction, button:discord.ui.Button):
        if not self.currentMember:
            await interaction.response.send_message("Please select a headmate first.", ephemeral = True)
            return
        memberImages = self.infoDict[self.currentMember]["images"]
        self.imageIndex = (self.imageIndex - 1) % len(memberImages)
        await self.buildAndSend(interaction)

    @discord.ui.button(label = "→")
    async def addButton(self, interaction: discord.Interaction, button:discord.ui.Button):
        if not self.currentMember:
            await interaction.response.send_message("Please select a headmate first.", ephemeral = True)
            return
        memberImages = self.infoDict[self.currentMember]["images"]
        self.imageIndex = (self.imageIndex + 1) % len(memberImages)
        await self.buildAndSend(interaction)

#TODO Check SRC queues - length, date of oldest run?

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="ping",description="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("h", ephemeral =True)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="counter",description="counter")
@app_commands.describe(visible="Visible to others?")
async def counter(interaction: discord.Interaction, visible: bool = False):
    await interaction.response.send_message("0", ephemeral = not visible, view = CounterButton())


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="anime",description="My Anime List")
@app_commands.describe(visible="Visible to others?")
async def anime(interaction: discord.Interaction, visible: bool = False):
    embed = discord.Embed(title = "Shigatsu wa Kimi no Uso", description = "Your Lie in April", color = myColor, url = "https://myanimelist.net/anime/23273")
    embed.add_field(name = "Mean Rating", value = "8.64")
    embed.add_field(name = "My Rating", value = "10")
    embed.set_image(url = "https://cdn.myanimelist.net/images/anime/1405/143284l.webp")
    await interaction.response.send_message(embed = embed, ephemeral = not visible, view = AnimeSelector())


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="system",description="My System!")
@app_commands.describe(visible="Visible to others?")
async def system(interaction: discord.Interaction, visible: bool = False):
    embed = discord.Embed(title = "Pearlescence System", description = "Welcome to my system index! Use the dropdown below to select a headmate, and the buttons to flip through their images!\nQuestions are more than welcome, please don't be scared to ask!\nNote: Messages by any member other than aspyn will be proxy tagged with the first letter of their name.", color = myColor)
    embed.add_field(name = "Resources", value = "[More Than One](<https://morethanone.info/>)\n[Pluralpedia](<https://pluralpedia.org/w/Plurality>)")
    await interaction.response.send_message(embed = embed, view = SystemViews(), ephemeral = not visible)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="sync",description="sync")
async def sync(interaction: discord.Interaction):
    if await sus(interaction.user.id):
        await vote(interaction)
        return
    await tree.sync()
    await interaction.response.send_message("sunk!", ephemeral = True)
    print("Sunk!")


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="pronouns",description="Pronouns... woke")
@app_commands.describe(visible="Visible to others?")
async def pronouns(interaction: discord.Interaction, visible: bool = False):
    embed = discord.Embed(title = "Pronouns", color = myColor, url = "https://pronouns.cc/@aspyn")
    embed.set_image(url = "attachment://pronouns.png")
    await interaction.response.send_message(embed = embed, file = discord.File('assets/pronouns.png'), ephemeral = not visible)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="uid",description="Send UID")
@app_commands.describe(game="Which UID?", visible="Visible to others?")
@app_commands.choices(game=[
        app_commands.Choice(name="Genshin", value="609006374"),
        app_commands.Choice(name="Honkai Star Rail", value="604969370"),
        app_commands.Choice(name="Valorant", value="gwenny#itgrl"),
        app_commands.Choice(name="Steam", value="883076786"),
        app_commands.Choice(name="Pokemon Go", value="545621393895"),
        app_commands.Choice(name="Pokemon TCG Pocket", value="6220292429679699"),
        app_commands.Choice(name="Bungie", value="aspyn#5311")
        #TODO add switch fc
    ]
)
async def uid(interaction: discord.Interaction, game: app_commands.Choice[str], visible: bool = False):
    embed = discord.Embed(title = f"{game.name} UID", description = game.value, color = myColor)
    await interaction.response.send_message(embed = embed, ephemeral = not visible)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="pfp",description="Get PFP")
@app_commands.describe(user="Whose PFP?", visible="Visible to others?")
async def pfp(interaction: discord.Interaction, user: discord.User, visible: bool = False):
    embed = discord.Embed(title = f"{user.name}'s PFP", color = myColor)
    embed.set_image(url = user.avatar.url)
    await interaction.response.send_message(embed = embed, ephemeral = not visible)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="roll",description="Roll Dice!")
@app_commands.describe(dicestring="Dice Expression", visible="Visible to others?")
async def roll(interaction: discord.Interaction, dicestring: str, visible: bool = False):
    try:
        result = str(d20.roll(dicestring))
    except: 
        await interaction.response.send_message("Invalid Expression", ephemeral = True)
        return
    await interaction.response.send_message(result, ephemeral = not visible)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="rollchar",description="Roll a Character!")
@app_commands.describe(visible="Visible to others?")
async def rollchar(interaction: discord.Interaction, visible: bool = False):
    result = ""
    for i in range(6):
        result += f"{d20.roll("4d6rr1kh3")}\n"
    await interaction.response.send_message(result, ephemeral = not visible)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="rollhelp",description="Link to d20 docs")
async def rollhelp(interaction: discord.Interaction):
    await interaction.response.send_message("https://github.com/avrae/d20?tab=readme-ov-file#operators", ephemeral = True)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.context_menu(name="fixfilespub")
async def fixfiles(interaction: discord.Interaction,  message: discord.Message):
    await interaction.response.defer()
    images = []
    hardware = path.exists("/dev/dri/renderD128")
    params = ["-vaapi_device", "/dev/dri/renderD128", "-vf", "hwupload,scale_vaapi=w=-2:h='min(720,iw)':format=nv12", "-c:v", "h264_vaapi", "-b:v", "1M"] if hardware else ["-c:v", "h264", "-vf", "scale=-2:'min(720,iw)'"]

    for attachment in message.attachments:
        extension = ""
        attachment_data = await attachment.read()
        mime = magic.from_buffer(attachment_data, mime = True).split("/")
        contentType = mime[0]
        contentExtension = mime[1]
        match contentType:
            case "image":
                if contentExtension == "gif":
                    images.append(await attachment.to_file(filename = f"{attachment.filename.split(".")[0]}.gif"))
                    continue
                command = ["ffmpeg", "-i", "pipe:0", "-f", "image2", "pipe:1"]
                extension = "jpg"
            case "video":
                command = ["ffmpeg", "-i", "pipe:0", *params, "-c:a", "aac", "-pix_fmt", "yuv420p", "-movflags", "frag_keyframe+empty_moov+faststart", "-f", "mp4", "pipe:1"]
                extension = "mp4"
            case "audio":
                command = ["ffmpeg", "-i", "pipe:0", "-loop", "1", "-r", "10", "-i", "assets/sus.webp", "-shortest", *params, "-c:a", "aac", "-pix_fmt", "yuv420p", "-movflags", "frag_keyframe+empty_moov+faststart", "-f", "mp4", "pipe:1"]
                extension = "mp4"
            case _:
                continue

        process = run(command, input = attachment_data, stdout = PIPE)
        if process.returncode == 0:
            discord_file = discord.File(fp = BytesIO(process.stdout), filename = f"{attachment.filename.split(".")[0]}.{extension}")
            images.append(discord_file)
    if len(images) > 0:
        await interaction.followup.send(files = images)
    else:
        await interaction.followup.send("No files to fix")


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.context_menu(name="fixfiles")
async def fixfiles(interaction: discord.Interaction,  message: discord.Message):
    await interaction.response.defer(ephemeral = True)
    images = []
    hardware = path.exists("/dev/dri/renderD128")
    params = ["-vaapi_device", "/dev/dri/renderD128", "-vf", "hwupload,scale_vaapi=w=-2:h='min(720,iw)':format=nv12", "-c:v", "h264_vaapi", "-b:v", "1M"] if hardware else ["-c:v", "h264", "-vf", "scale=-2:'min(720,iw)'"]

    for attachment in message.attachments:
        extension = ""
        attachment_data = await attachment.read()
        mime = magic.from_buffer(attachment_data, mime = True).split("/")
        contentType = mime[0]
        contentExtension = mime[1]
        match contentType:
            case "image":
                if contentExtension == "gif":
                    images.append(await attachment.to_file(filename = f"{attachment.filename.split(".")[0]}.gif"))
                    continue
                command = ["ffmpeg", "-i", "pipe:0", "-f", "image2", "pipe:1"]
                extension = "jpg"
            case "video":
                command = ["ffmpeg", "-i", "pipe:0", *params, "-c:a", "aac", "-pix_fmt", "yuv420p", "-movflags", "frag_keyframe+empty_moov+faststart", "-f", "mp4", "pipe:1"]
                extension = "mp4"
            case "audio":
                command = ["ffmpeg", "-i", "pipe:0", "-loop", "1", "-r", "10", "-i", "assets/sus.webp", "-shortest", *params, "-c:a", "aac", "-pix_fmt", "yuv420p", "-movflags", "frag_keyframe+empty_moov+faststart", "-f", "mp4", "pipe:1"]
                extension = "mp4"
            case _:
                continue

        process = run(command, input = attachment_data, stdout = PIPE)
        if process.returncode == 0:
            discord_file = discord.File(fp = BytesIO(process.stdout), filename = f"{attachment.filename.split(".")[0]}.{extension}")
            images.append(discord_file)
    if len(images) > 0:
        await interaction.followup.send(files = images)
    else:
        await interaction.followup.send("No files to fix")


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="temperature",description="Convert Temperatures")
@app_commands.describe(input="Input amount and units (with a space)", visible="Visible to others?")
async def roll(interaction: discord.Interaction, input: str, visible: bool = False):
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
    embed = discord.Embed(title = "Temperature Conversion", description = outputString, color = myColor)
    await interaction.response.send_message(embed = embed, ephemeral = not visible)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="ethics",description="Code of Ethics :3")
@app_commands.describe(visible="Visible to others?")
async def ethics(interaction: discord.Interaction, visible: bool = False):
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
    number = random.randrange(len(ethicsArray))
    embed = discord.Embed(title = f"{number + 1}.", description = ethicsArray[number], color = myColor)
    await interaction.response.send_message(embed = embed, ephemeral = not visible)


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@tree.command(name="advice",description="Advice for Budding Streamers")
@app_commands.describe(visible="Visible to others?")
async def advice(interaction: discord.Interaction, visible: bool = False):
    adviceArray = [
        "Be kind and wholesome; positivity is inherently contagious.",
        "Be yourself, but be measured: people want authenticity, but too much feels like therapy.",
        "Model the behavior you want to see in your followers.",
        "Have an extremely cool penis.",
        "Be famous, sexually-active, and have a large social media following.",
        "Be very famous, have a huge social media following, and be extremely sexually-active.",
        "Dig up a skeleton from the cemetery on stream.",
        "Find a sick child and film him. Viewers appreciate sick children.",
        "Give your dog a math problem and stream him struggling with it. Viewers like to know they're not alone.",
        "Add a laugh track to your stream so that your audience knows when to laugh. This will help remind your audience that they have missed out on a golden opportunity to laugh.",
        "Never make your streaming schedule too rigid. You want to give yourself an opportunity to take a day off.",
        "Film the future. It will give your viewers on opportunity to make trades from which they can profit handsomely.",
        "Relish the opportunity to correct your own misstatements. It's not a sign of weakness: it gives viewers comfort to know that you're fallible too.",
        "Show your iPad screen when you're playing a mobile game: people love to know that their heroes have iPads.",
        "Let your viewers know that you're (eventually) going to tell them how to get rich off of bitcoin; but to shut the fuck, be quiet, and focus on your stream until you're ready to tell them.",
        "Charge your phone on camera (optional).",
        "The best streamers are even better listeners. Your followers didn't show up to listen to you talk all day — they showed up to listen to you listen.",
        "Bend your viewers to your will.",
        "Never forget your roots. Your stream started out on Justin.tv, which was a platform designed for traditional content distribution. Give a shout out to Justin every once in a while.",
        "Require that users enable Macromedia Flash Player to view your stream.",
        "Share some of your passwords with your audience to establish trust.",
        "You don't have to stream games! Sometimes your viewers just want a crash course on how to build a nuclear bomb, or a history lesson on Syrian military victories.",
        "Don't be afraid to give your viewers a reason to fear and hate you.",
        "Play Russian Roulette on stream. Tell your viewers that you'll add a bullet to the chamber for every donation.",
        "Donate to yourself on stream to show to your audience that you're just as invested in your own success as they are.",
        "Followers remember what they see, and they'll forget the things they never saw.",
        "When it's hot out, make sure to drink water on stream. When it's cold out, make sure to drink hot chocolate. Be consistent.",
        "Don't be afraid to show your belly button and/or asshole.",
        "People who chat the most, donate the least. Eliminate them.",
        "Tell your viewers to hold their applause until the end. Ban anybody who doesn't listen.",
        "Constantly remind your viewers that 'age is just a number.'",
        "Release your complete tax returns and long-form birth certificate on stream so the audience knows you're a red-blooded American."
    ]
    number = random.randrange(len(adviceArray))
    embed = discord.Embed(title = f"{number + 1}.", description = adviceArray[number], color = myColor)
    await interaction.response.send_message(embed = embed, ephemeral = not visible)

@client.event
async def on_ready():
    print("Ready!")

client.run(secrets["token"])