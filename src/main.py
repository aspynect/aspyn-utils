import discord
from discord import app_commands
from os import getenv
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

DISCORD_TOKEN = getenv("DISCORD_TOKEN", "NO TOKEN PROVIDED")
MAL_TOKEN = getenv("MAL_TOKEN", "NO TOKEN PROVIDED")
# optional env var
HEADMATES_LIST = getenv("HEADMATES_LIST", "aspyn,Cassie,Shane,Ruth,nea,Pearl").split(",")

class Anime():
    def __init__(self):
        self.animeInfo = self.getAnimeList()
    
    def getAnimeList(self):
        response = requests.get("https://api.myanimelist.net/v2/users/aspynect/animelist?status=completed&sort=list_score&limit=25&fields=id,title,mean,main_picture,list_status,alternative_titles", headers = {'X-MAL-CLIENT-ID': MAL_TOKEN})
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
        self.timeout = None
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

    @discord.ui.select(placeholder = "Select a headmate", options = [discord.SelectOption(label = HEADMATES_LIST[i], value = i) for i in range(len(HEADMATES_LIST))], max_values=1)
    async def headmateSelector(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.imageIndex = 0
        self.currentMember = HEADMATES_LIST[int(select.values[0])]
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

@tree.command(name="ping",description="ping")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("h", ephemeral =True)


@tree.command(name="counter",description="counter")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(visible="Visible to others?")
async def counter(interaction: discord.Interaction, visible: bool = False):
    await interaction.response.send_message("0", ephemeral = not visible, view = CounterButton())


@tree.command(name="anime",description="My Anime List")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(visible="Visible to others?")
async def anime(interaction: discord.Interaction, visible: bool = False):
    embed = discord.Embed(title = "Shigatsu wa Kimi no Uso", description = "Your Lie in April", color = myColor, url = "https://myanimelist.net/anime/23273")
    embed.add_field(name = "Mean Rating", value = "8.64")
    embed.add_field(name = "My Rating", value = "10")
    embed.set_image(url = "https://cdn.myanimelist.net/images/anime/1405/143284l.webp")
    await interaction.response.send_message(embed = embed, ephemeral = not visible, view = AnimeSelector())


@tree.command(name="system",description="My System!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(visible="Visible to others?")
async def system(interaction: discord.Interaction, visible: bool = False):
    embed = discord.Embed(title = "Pearlescence System", description = "Welcome to my system index! Use the dropdown below to select a headmate, and the buttons to flip through their images!\nQuestions are more than welcome, please don't be scared to ask!\nNote: Messages by any member other than aspyn will be proxy tagged with the first letter of their name.", color = myColor)
    embed.add_field(name = "Resources", value = "[More Than One](<https://morethanone.info/>)\n[Pluralpedia](<https://pluralpedia.org/w/Plurality>)")
    await interaction.response.send_message(embed = embed, view = SystemViews(), ephemeral = not visible)


@tree.command(name="sync",description="sync")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def sync(interaction: discord.Interaction):
    if await sus(interaction.user.id):
        await vote(interaction)
        return
    await tree.sync()
    await interaction.response.send_message("sunk!", ephemeral = True)
    print("Sunk!")


@tree.command(name="pronouns",description="Pronouns... woke")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(visible="Visible to others?")
async def pronouns(interaction: discord.Interaction, visible: bool = False):
    embed = discord.Embed(title = "Pronouns", color = myColor, url = "https://pronouns.cc/@aspyn")
    embed.set_image(url = "attachment://pronouns.png")
    await interaction.response.send_message(embed = embed, file = discord.File('assets/pronouns.png'), ephemeral = not visible)


@tree.command(name="uid",description="Send UID")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(game="Which UID?", visible="Visible to others?")
@app_commands.choices(game=[
        app_commands.Choice(name="Genshin", value="609006374"),
        app_commands.Choice(name="Honkai Star Rail", value="604969370"),
        app_commands.Choice(name="Valorant", value="gwenny#itgrl"),
        app_commands.Choice(name="League of Legends", value="XxJynxFan300xX#JYNX"),
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


@tree.command(name="pfp",description="Get PFP")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Whose PFP?", visible="Visible to others?")
async def pfp(interaction: discord.Interaction, user: discord.User, visible: bool = False, server: bool = True):
    embed = discord.Embed(title = f"{user.name}'s PFP", color = myColor)
    image = user.display_avatar.url if server else user.avatar.url
    embed.set_image(url = image)
    await interaction.response.send_message(embed = embed, ephemeral = not visible)


@tree.command(name="roll",description="Roll Dice!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(dicestring="Dice Expression", visible="Visible to others?")
async def roll(interaction: discord.Interaction, dicestring: str, visible: bool = False):
    try:
        result = str(d20.roll(dicestring))
    except: 
        await interaction.response.send_message("Invalid Expression", ephemeral = True)
        return
    await interaction.response.send_message(result, ephemeral = not visible)


@tree.command(name="rollchar",description="Roll a Character!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(visible="Visible to others?")
async def rollchar(interaction: discord.Interaction, visible: bool = False):
    result = ""
    for i in range(6):
        result += f"{d20.roll("4d6rr1kh3")}\n"
    await interaction.response.send_message(result, ephemeral = not visible)


@tree.command(name="rollhelp",description="Link to d20 docs")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def rollhelp(interaction: discord.Interaction):
    await interaction.response.send_message("https://github.com/avrae/d20?tab=readme-ov-file#operators", ephemeral = True)


@tree.command(name="echo",description="echo")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def echo(interaction: discord.Interaction, echostring: str, visible: bool = False):
    await interaction.response.send_message(echostring, ephemeral = not visible)


@tree.context_menu(name="fixfilespub")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
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


@tree.context_menu(name="fixfiles")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
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


@tree.command(name="temperature",description="Convert Temperatures")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
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


@tree.command(name="asktheangel",description="Ask the Angel")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(visible="Visible to others?")
async def ask_the_angel(interaction: discord.Interaction, question: str, visible: bool = False):
    # https://github.com/chloebangbang/ask-the-angel/blob/main/src/dr_choicers.rs
    angelArray = [
        #ch1
        "Yes", "No",
        "Not yet", "Yes. Ask.",
        "Not yet", "Yes",
        "Good", "Bad",
        "Yes", "No",
        "Listen", "No",
        "Listen", "We know it already",
        "I'll be Your Subject", "Keep Dreaming",
        "I know", "Really!?",
        "I know", "Really!?",
        "Yes", "Don't",
        "I can handle it", ".....",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        "Crumpled paper", "LANCER labelled paper", "Neat paper",
        "Yes", "No",
        "Noelle", "Family", "Illness", "Nothing",
        "No No No No No No No No No", "Yes",
        "Sit", "Don't Sit",
        "Stick fingers", "Don't",
        "Yes", "No",
        "Kris", "Hippopotamus",
        "Onion", "Beauty", "Asriel II", "Disgusting",
        "Open Fridge", "Don't", "See photos",
        "Asriel", "Neighbors", "Sister", "Nothing",
        "Neighbor", "Memories", "Go Away", "Nothing",
        "Buy", "No",
        "Buy", "No",
        "Buy", "No",
        "Buy", "No",
        "What's TP?", "Secret", "Gaining TP", "Bye",
        "Pacify", "Healing", "Fact", "Bye",
        "Warning", "Attack", "Fact", "Bye",
        "Reviving", "Acting", "Fact", "Bye",
        "Throw $1", "Do not",
        "Make Ralsei try it", "Try it", "Decline",
        "Flowers", "Saucer", "Chalk", "Nothing",
        "Add Spade", "Add Diamond", "Swap",
        "Perpetuate", "Do not",
        "Take", "Do not",
        "Yes", "She'll be fine",
        "Go Left", "Go Right",
        "Fix Item", "Leave", "Fix Us",
        "Buy", "Do not",
        "Buy", "Do not",
        "Buy", "Do not",
        "Alphys", "Dark World", "Help you", "Nothing",
        "Asriel", "Job", "Co-Workers", "No",
        "Fruit Juice", "Nothing",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        "Great to see you again", "Who the hell are you?",
        "Store", "Friends", "Leave",
        "Me", "My Mom", "My Teacher", "Nobody",
        "1", "2", "3", "4",
        "Yes", "No",
        "Susie", "Key", "Anything", "Nothing",
        "She's nice", "Terrible", "Eats Chalk", "...",
        "Yes", "No",
        "Sleep", "Do not",
        "Sleep!!!", "Do not!!!",
        "Play a game", "Do not play a game",
        "Play a game", "Do not play a game",
        "Use Key", "Do not",
        "Blaze", "Do Not Blaze",
        "Apologize Profusely", "Intimidate",
        "Listen", "Do Not",
        "Prison B1", "Floor 1F", "??????",
        "Ride", "Do not",
        "Yes", "Don't",
        "Let's Fight", "Let's Not",
        "Me", "Asriel", "Flowers",
        # the warp doors are formatted weird as hell in the code but I think this is the most true to how it's implemented
        # albeit not to how you're supposed to perceive them
        "Field", "Forest", "Forest", "Bake Sale", "Castle",
        "Give Cake", "Do not",
        "Take Cake", "No",
        "Yes", "No",
        "Yes", "No",
        "Sweet", "Soft", "Sour", "Salty", "Pain", "Cold",
        "A", "AB", "B", "C", "D",
        "Red", "Blue", "Green", "Cyan",
        "Kindness", "Mind", "Ambition", "Bravery", "Voice",
        "Love", "Hope", "Disgust", "Fear",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        # ch2
        "Yes", "No",
        "Lost sleep from being Susie's partner", "Actually my sleep quality increased",
        "Hanging out alone in the closet", "Crime",
        "Hug", "No",
        "Hell yeah!", "No...",
        "Bosom", "Perish",
        "Lie and say you want to hear more", "Stop Conversation",
        "Inspect", "Do not",
        "Dark World", "...",
        "Complain About Police", "Talk About School", "See ya",
        "Yes", "No",
        "Let's go! Let's go!", "We can use the computer at my house",
        "Talk", "Susie", "Don't",
        "Talk More", "Don't talk more",
        "Cause they care", "Your family is weird",
        "Noelle", "Family", "Jockington", "Nothing",
        "Gerson", "Hammer", "Asriel", "Nothing",
        "Current situation", "Susie", "Noelle", "Nothing",
        "Take it", "Do not",
        "You", "Someone Else", "No", 
        "Go with Ralsei", "Go with Susie",
        "Yeah", "Not yet",
        "Wondering", "Don't care",
        "Wondering", "Really don't care",
        "Of course", "No Triple Trucies",
        "We're friends", "We're something else",
        "Buy", "Talk", "Leave",
        "Take", "Don't",
        "Buy", "Don't Buy",
        "Buy", "No",
        "Kris", "Susie", "Noelle", "Ralsei",
        "Go Inside", "Don't go in",
        "Give to Ralsei", "Give to Susie", "Give to Noelle", "Give to Berdly",
        "We have a truce", "She is our enemy",
        "Yes", "No",
        "Noelle", "Ralsei", "You", "...",
        "I am going to touch the cheese", "I do not touch the cheese",
        "Yes", "No",
        "Check Recruits", "Prize", "Nothing",
        "Fuse Items", "Fix Us", "Chat", "Leave",
        "Take Cookie", "Do Not",
        "Grazing", "Hitbox", "Hole", "Nothing",
        "Challenge", "Nothing",
        "Join", "Do not join",
        "I feel the same", "It's strange",
        "Thinking of Noelle", "Thinking of Susie", "Thinking of Berdly", "Thinking of you",
        "It's nice that Ralsei is Ralsei", "...",
        "Do not pose", "Hug Ralsei", "Peace sign", "Rude gesture",
        "Dark World", "Evil Queen's Castle",
        "Point and hearts come out", "Eat Moss",
        "Do something nuts", "Do something crazy",
        "Say something romantic", "Say something cool",
        "Lie", "Lie",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        "Check Recruits", "Recommendation", "Exit",
        "Yes", "No",
        "Left", "Right", "Top", "Bottom",
        "Left", "Right", "Top", "Bottom",
        "Left", "Right", "Top", "Bottom",
        "Buy", "Don't Buy",
        "Buy 400 bagels", "Buy 1 bagel", "Don't buy",
        "Look in the back", "Look inside",
        "Read", "Don't",
        "Occupation", "See brother", "Buy things", "Nothing",
        "Play", "Do not",
        "Give chocolate", "Hoard chocolate",
        "Yes", "No",
        "Yes", "Nooooo",
        "It's horrible", "It's natural",
        "Seems a little far fetched", "Yeah let's do it",
        "Of course", "Of course not",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        "Proceed", "I'm protecting her from you!",
        "Gaming is my life", "Gaming is not my life",
        "They like you", "Unknown", "Yes",
        "Yes", "No",
        "Yes", "No",
        "I will ride with you", "Susie would", "Susie wouldn't",
        "Noelle will ride with me", "Sorry",
        "Yes", "No",
        "Mansion", "Cyber Field", "Trash Zone", "Cancel",
        "Sorry, I'll do the puzzle", "Proceed",
        "Let's solve it together!", "Proceed",
        "Get it", "We're fine",
        "Get it", "We're fine",
        "To see your father", "To see you",
        "In your dream", "...",
        "Because it wasn't a dream", "...",
        "Take", "Do Not",
        "Yes", "No",
        "Sorry, I'll do the puzzle", "Proceed",
        "Sorry, I'll do the puzzle", "Proceed",
        "Sorry, I'll do the puzzle", "Proceed",
        "Sorry, I'll do the puzzle", "Proceed",
        "Yes", "No",
        "Recruits", "Item storage", "Controls", "Do not read",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        "Yes", "No",
        #ch3
        "Of course. Games are fun", "No",
        "Yes", "No",
        "Buy", "Don't Buy",
        "Yes", "No",
        "Buy something", "Talk more", "Nothing else",
        "Enter", "Do not",
        "Play", "Don't play",
        "Yes", "No",
        "Strike a cool pose", "Strike a glamorous pose",
        "Buy", "Don't Buy",
        "$50 -> 10 PTs", "$250 -> 60 PTs", "$1000 -> 250 PTs", "Don't exchange",
        "Sarcasm", "Everything I say is serious",
        "Yes", "No",
        "Here to cheat", "Got Lost looking for Lancer",
        "Fight it out", "Get Caught",
        "Got Lost looking for the exit",
        "Back here to do good deeds",
        "Obviously", "No thanks",
        "Explain please", "Let's go!",
        "Still not ready", "Ready",
        "Sleep", "Do not",
        "Buy", "Don't Buy",
        "Give 1500 POINTs", "No thanks",
        "Instructions please", "Let's go",
        "Enter Code", "Do Not",
        "Super fun", "Eh",
        "Yes", "Not yet...",
        "Need instructions", "Don't need instructions to rock",
        "Cheater", "Not Really",
        "Where I came from", "Here",
        "No", "Yes",
        "Yes", "Not Yet",
        "Fight him", "Press his buttons", "Don't do anything",
        "Sign", "Don't",
        "Buy TV Dinner for $250", "Don't",
        "Love", "Hate",
        "Yes", "......Yes",
        "Playing games", "Nothing",
        "My rank, my rewards?", "What's in each door?", "Don't",
        "Yes", "No",
        "Check scores", "Tips and Tricks", "Nothing",
        "Check scores", "Tips and Tricks", "Nothing",
        "Check scores", "Tips and Tricks", "Nothing",
        "Play COOKING SHOW", "Quit",
        "Play ROCK VIDEO", "Quit",
        "Normal Mode", "Difficult Mode", "Don't play",
        "Pay 500 points", "Don't",
        "Play MYSTERY GAME", "Play MONSTER MOVIE", "Quit",
        "Enter", "Do Not",
        "Enter", "Do Not",
        "Help or Don't Help", "Pick him up", "No response",
        "See what Susie's doing", "Let's just chill dude",
        "Eyes closed", "Eyes open",
        "Your face", "No",
        "Seen it before", "Cute", "Unique",
        "Talking", "Trying to close eyes and think about Susie",
        "He's fun", "He sucks",
        "Let's go", "Wait",
        "Let me talk", "Nah",
        "Lanino", "Nothing",
        "You're strong and independant", "Your forecast is love",
        "Weather report", "Nothing",
        "You're strong and independant", "Your forecast is love",
        "Ask Susie how she's doing", "Ask Ralsei how he's doing", "Don't",
        "I'm not a dream", "Your friendships are real", "Sucks to be you",
        "It's ok to take it easy", "Stay on task",
        "I'm not going with her", "I'm saying it's from me", "Of course",
        "Noelle", "Ralsei or bust", "Berdly", "Not going",
        "Yes", "No",
        "Hear more", "Enough",
        "Hear more", "No more",
        "Hear more", "Please no more",
        "Yes", "No",
        "50 PTs -> $50", "200 PTs -> $250", "1000 PTs -> $1500", "Don't exchange",
        "Buy 1 for $300", "Buy 3 for $800", "Nope",
        "TV World Entrance", "Goulden Sam", "Green Room", "Cancel",
        "Read it", "Don't read it",
        "She Look Very Nice", "Sorry this is happening",
        "Let's pay attention", "Look in pocket for fun",
        "Put a sticker in a good place", "Put a sticker in a bad place",
        "Noelle, run! She'll drink your blood", "Get closer! She'll drink your blood",
        "Yes", "No",
        "Yes please", "No, you have it",
        "Draw something", "Do nothing",
        "Accurate", "Looks bad chief",
        "Make Susie drawing talk", "Do nothing",
        "Write something in the corner", "Do nothing",
        "Yes", "No",
        "Explain the clues", "Not yet",
        "...", "Me",
        "It was a joke", "Because it wasn't a dream",
        "Sorry, just a prank", "I heard",
        "Sorry, just a prank", "It's not a coincidence",
        "Red", "Blue",
        "Green", "Black",
        "It snowed", "It happened",
        "Noelle will get stronger", "Noelle becomes stronger",
        "Equip", "Equip",
        "Proceed", "Proceed",
        "Proceed", "Proceed",
        "Proceed", "Proceed",
        "Equip", "Equip",
        "Equip", "Equip",
        "Please be yourself", "Of course not",
        "Say what's on your mind", "Say nothing",
        "Yes", "No",
        "Go with Berdly", "Sing the wrong number song",
        "Enter the shelter", "Bangin' sermon my man", "Asgore",
        "Shelter", "Susie will not be tamed",
        "Shelter", "Laugh", "Don't laugh",
        "Offer juice", "Drink juice in front of her",
        "Shelter", "No!",
        "Architectural history research", "Put hay inside, new house for Susie",
        "She gave you chocolates though", "It's because of me",
        "Add 25% red juice", "Add 25% yellow juice", "Empty drink",
        "Asgore", "Key", "Noelle",
        "Nice singing", "Key", "Locked door",
        "Take it", "Do not",
        "Favorites History", "Cat Petterz 4", "Do Not Click",
        "Yes", "No",
        "Old family photo", "Asriel photo", "Don't show either",
        "Discuss plans", "Leave very fast",
        "Tomorrow", "Susie", "Leave",
        "Heat him up", "Leave him",
        "Talk about Catty", "Eavesdrop on blue bunny", "Leave",
        "Yes", "No",
        "Susie", "Parents", "Leave",
        "Read", "Do not",
        "Hear more", "Do not",
        "Inquire about what's going on", "Leave",
        "Change the RPM", "Press the stop button",
        "Offer to give your TV", "Nothing",
        "Investigate", "Do not",
        "Talk about the knight", "Leave", "Jester",
        "Susie ate the clothes", "I ate the clothes",
        "Yes", "No",
        "Show", "Don't show",
        "Store", "What are you doing", "Knight", "Nothing",
        "Sure", "Seems unnecessary",
        "Close eyes for just a moment", "Don't",
        "No", "Think of The Knight", "Think of Noelle",
        "Yes", "No",
        "Go Susie! Go Susie!", "Sorry, not enough time",
        "Listen to it", "Keep walking around",
        "It's okay not to smile", "Good. Keep smiling",
        "That's right", "Prayer",
        "Pray for Susie", "Pray for Noelle", "Pray for Asriel", "Do nothing",
        "Open", "Don't",
        "Mess with them", "Don't",
        "Listen (it might be long)", "Not now",
        "I'll play again someday", "If you play too", "I'll never play again",
        "Advice where to go", "Cute...", "Nothing",
        "No", "Yes", "Two lumps please",
        "Ralsei eat the cake", "That's my cake",
        "Yes", "No",
        "Drink it", "Don't drink",
        "Not now", "Actually I will have tea",
        "Sleep through service", "Watch service",
        "Yes", "No",
        "Yeah", "Nah",
        "Undyne", "Shelter", "Nothing",
        "But we aren't logical", "But Mom could be in there",
        "Dig through", "Don't dig through",
        "Check the panel", "Don't",
        "Outfit", "Are you okay", "Nothing",
        "Yes", "No",
        "Sure", "Not from you",
        "Play (Normal)", "Play (Hard)",
        "Suggest Tenna", "Don't suggest anything",
        "Photo pose!", "Nothing",
        "Jump down", "Wait a sec",
        "Turn the doornob", "Do not",
        "Buy", "Do not", "Why do you need money",
        "Ask", "Don't ask",
        "Don't sleep", "Sleep an incredibly long time",
        "Enter code", "Do not"
    ]
    number = random.randrange(len(angelArray))
    embed = discord.Embed(title = question, description = angelArray[number], color = myColor)
    await interaction.response.send_message(embed = embed, ephemeral = not visible)


@tree.command(name="ethics",description="Code of Ethics :3")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
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


@tree.command(name="advice",description="Advice for Budding Streamers")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
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

client.run(DISCORD_TOKEN)