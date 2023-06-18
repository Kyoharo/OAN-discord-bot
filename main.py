import re
import discord
import os
from dotenv import load_dotenv
from bardapi import ChatBard
import asyncio
import random
from discord import app_commands
from discord.ext import commands
from core.pageview import PageView
from TTS.api import TTS
import whisper

activity = ["/", "OAN"]
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
Bard_Token = os.getenv('BARD_TOKEN')

chat = ChatBard()
intents = discord.Intents.default()
intents.message_content = True
class aclient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        try:
            await self.wait_until_ready()
            await self.change_presence(activity=discord.Game(random.choice(activity)))
            synced = await self.tree.sync()
            print(f"synced {len(synced)} commands(s)")
            print(f"Say hi to {self.user}!")
        except Exception  as e:
            print(e)

client = aclient()





#---------------------------------------------          ask       -----------------------------------------------------------------
@client.tree.command(name='ask', description='Ask me a question.')
async def ask_question(interaction: discord.Interaction, your_question: str):
    user_id = interaction.user.id
    user_name = interaction.user.name        
    pass_question = f"**{user_name}**: {your_question}"
    await interaction.response.defer(thinking=True)
    response = await asyncio.to_thread(chat.start, user_id, pass_question)
    embeds = []
    if len(response) > 2000:
        texts = []
        for i in range(0, len(response), 2000):
            texts.append(response[i:i+2000])
        for text in texts:
            your_question = your_question[:230]
            embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{text}", color=discord.Color.dark_gold())
            embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
            embeds.append(embed)
        view = PageView(embeds)
        await interaction.followup.send(embed=view.initial(), view=view)
    else:
        your_question = your_question[:230]
        embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{response}", color=discord.Color.dark_gold())
        embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
        embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
        await interaction.followup.send(embed=embed)
    
    try:    
        guild = interaction.guild   
        print(f"Guild: {guild.name},   username: {user_name}")
    except Exception as e:
        print(f"username: {user_name}")


#---------------------------------------------          reoan       -----------------------------------------------------------------
@client.tree.command(name="language", description='Start a new conversation in a specific language')
@app_commands.choices(language=[
    app_commands.Choice(name='English', value="English"),
    app_commands.Choice(name='Arabic', value='Arabic'),
    app_commands.Choice(name='Japanese', value="Japanese"),
    app_commands.Choice(name='German', value="German"),
    app_commands.Choice(name='Italian', value="Italian"),
    app_commands.Choice(name='Spanish', value="Spanish"),
    app_commands.Choice(name='Korean', value="Korean"),
    app_commands.Choice(name='Polish', value="Polish"),
    app_commands.Choice(name='Portuguese', value="Portuguese"),
    app_commands.Choice(name='Russian', value="Russian"),
    app_commands.Choice(name='Albanian', value="Albanian"),
    app_commands.Choice(name='Serbian', value="Serbian"),
    app_commands.Choice(name='turkish', value="turkish"),
    app_commands.Choice(name='Ukrainian', value="Ukrainian"),
    app_commands.Choice(name='Urdu', value="Urdu"),
    app_commands.Choice(name='Romanian', value="Romanian"),
    app_commands.Choice(name='Hungarian', value="Hungarian"),
    app_commands.Choice(name='Croatian', value="Croatian"),
    app_commands.Choice(name='Hindi', value="Hindi"),
    app_commands.Choice(name='Hebrew', value="Hebrew"),
    app_commands.Choice(name='French', value="French"),
    app_commands.Choice(name='Greek', value="Greek"),
])
async def language(interaction: discord.Interaction, language: app_commands.Choice[str], your_question: str):
    member = interaction.user
    user_id = member.id
    user_name = interaction.user.name
    await interaction.response.defer(thinking=True)
    pass_question = f"**{user_name}**: {your_question}"
    response = await asyncio.to_thread(chat.start, user_id, pass_question, language.name.lower(),reset="reset")
    embeds = []
    if len(response) > 2000:
        texts = [response[i:i+2000] for i in range(0, len(response), 2000)]
        for text in texts:
            your_question = your_question[:230]
            embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{text}", color=discord.Color.dark_gold())
            embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
            embeds.append(embed)
        view = PageView(embeds)
        await interaction.followup.send(embed=view.initial(), view=view)
    else:
        your_question = your_question[:230]
        embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{response}", color=discord.Color.dark_gold())
        embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
        embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
        await interaction.followup.send(embed=embed)
    try:    
        guild = interaction.guild   
        print(f"Guild: {guild.name},   username: {user_name}")
    except Exception as e:
        print(f"username: {user_name}")

#---------------------------------------------         !ask       -----------------------------------------------------------------
@client.command(name='ask', help='Ask me a question.')
async def ask_question(ctx, *, your_question):
    user_id = ctx.author.id
    user_name = ctx.author.name
    pass_question = f"**{user_name}**: {your_question}"
    await ctx.defer()
    response = await asyncio.to_thread(chat.start, user_id, pass_question)
    embeds = []
    if len(response) > 2000:
        texts = []
        for i in range(0, len(response), 2000):
            texts.append(response[i:i+2000])
        for text in texts:
            your_question= your_question[:230]
            embed = discord.Embed(title=f""">   ``{your_question}``""",description=f"{text}",color=discord.Color.dark_gold())
            embed.set_author(name="OAN",
            icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
            embeds.append(embed)
        view = PageView(embeds)
        await ctx.reply(embed=view.initial(), view=view)
    else:
        your_question= your_question[:230]
        embed = discord.Embed(title=f""">   ``{your_question}``""",description=f"{response}",color=discord.Color.dark_gold())
        embed.set_author(name="OAN",
        icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
        embed.set_footer(text=f'{user_name}', icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    try:
        guild = ctx.guild
        print(f"!ask** Guild: {guild.name},   username: {user_name}")
    except Exception as e:
        print(f"!ask** username: {user_name}")



#whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("small")
    result = model.transcribe(audio_path)
    text = result["text"]
    language = result["language"]
    return text, language


#TTS
def tts_audio(response, path, lanuage):
    if "ja" in lanuage:
        model_name = 'tts_models/ja/kokoro/tacotron2-DDC'
        tts = TTS(model_name)
        tts.tts_to_file(text=response, file_path=path)
    else:
        model_name = TTS.list_models()[0]
        tts = TTS(model_name)
        tts.tts_to_file(text=response, speaker=tts.speakers[2], language=tts.languages[0], file_path=path)


#--------------------------------------------  private message   ------------------------------------------------------
@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and message.author != client.user:
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                if attachment.content_type.startswith('audio'):
                    user_name = message.author.name
                    user_id =str(message.author.id)
                    DOWNLOAD_DIR = os.path.join("audio_files", user_id)

                    if not os.path.exists(DOWNLOAD_DIR):
                        os.makedirs(DOWNLOAD_DIR)

                    filename = os.path.join(DOWNLOAD_DIR, attachment.filename)
                    await attachment.save(filename)

                    your_question, language = transcribe_audio(filename)
                    print(your_question, language)
                    pass_question = f"**{user_name}**: {your_question}"

                    response = await asyncio.to_thread(chat.start, int(user_id), pass_question, language)
                    #convert the response to speech
                    if "en" in language or "ja" in language:
                        output_path = f"audio_files/{user_id}/output.wav"
                        tts_audio(response, output_path, language)
                        print("tts done")

                        if os.path.exists(output_path):
                            embed = discord.Embed(title=f""">   ``{your_question}``""",
                                                description=f"{response}",
                                                color=discord.Color.dark_gold())
                            embed.set_author(name="OAN",
                                            icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                            embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)

                            await message.channel.send(embed=embed, file=discord.File(output_path, filename="output.wav"))
                            return
                        
                    embeds = []
                    if len(response) > 2000:
                        texts = [response[i:i+2000] for i in range(0, len(response), 2000)]
                        for text in texts:
                            your_question = your_question[:230]
                            embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{text}", color=discord.Color.dark_gold())
                            embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                            embeds.append(embed)
                        view = PageView(embeds)
                        await message.channel.send(embed=view.initial(), view=view)
                    else:
                        your_question = your_question[:230]
                        embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{response}", color=discord.Color.dark_gold())
                        embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                        embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)
                        await message.channel.send(embed=embed)

                    try:
                        guild = message.guild
                        print(f"!ask** Guild: {guild.name}, username: {user_name}")
                    except Exception as e:
                        print(f"!ask** username: {user_name}")
    await client.process_commands(message)



#---------------------------------------------         !vc       -----------------------------------------------------------------

@client.command(name='vc', help='Ask me a voice question')
async def ask_question(ctx):
    user_name = ctx.author.name
    user_id = str(ctx.author.id)
    DOWNLOAD_DIR = os.path.join("audio_files", user_id)

    if len(ctx.message.reference.resolved.attachments) > 0:
        for attachment in ctx.message.reference.resolved.attachments:
            if attachment.content_type.startswith('audio'):
                # Create the download directory if it doesn't exist
                if not os.path.exists(DOWNLOAD_DIR):
                    os.makedirs(DOWNLOAD_DIR)
                # Download the audio file
                filename = os.path.join(DOWNLOAD_DIR, attachment.filename)
                await attachment.save(filename)
                your_question, language = transcribe_audio(filename)
                print(your_question, language)
                pass_question = f"**{user_name}**: {your_question}"
                await ctx.defer()
                response = await asyncio.to_thread(chat.start, int(user_id), pass_question,language)

                #convert the response to speech
                if "en" in language or "ja" in language:
                    output_path = f"audio_files/{user_id}/output.wav"
                    tts_audio(response, output_path, language)
                    print("tts done")

                    if os.path.exists(output_path):
                        embed = discord.Embed(title=f""">   ``{your_question}``""",
                                            description=f"{response}",
                                            color=discord.Color.dark_gold())
                        embed.set_author(name="OAN",
                                        icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                        embed.set_footer(text=f'{user_name}', icon_url=ctx.author.avatar.url)

                        await ctx.reply(embed=embed, file=discord.File(output_path, filename="output.wav"))
                        return

                embeds = []
                if len(response) > 2000:
                    texts = []
                    for i in range(0, len(response), 2000):
                        texts.append(response[i:i+2000])
                    for text in texts:
                        your_question= your_question[:230]
                        embed = discord.Embed(title=f""">   ``{your_question}``""",description=f"{text}",color=discord.Color.dark_gold())
                        embed.set_author(name="OAN",
                        icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                        embeds.append(embed)
                    view = PageView(embeds)
                    await ctx.reply(embed=view.initial(), view=view)
                else:
                    your_question= your_question[:230]
                    embed = discord.Embed(title=f""">   ``{your_question}``""",description=f"{response}",color=discord.Color.dark_gold())
                    embed.set_author(name="OAN",
                    icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    embed.set_footer(text=f'{user_name}', icon_url=ctx.author.avatar.url)
                    await ctx.reply(embed=embed)

                try:
                    guild = ctx.guild
                    print(f"!ask** Guild: {guild.name},   username: {user_name}")
                except Exception as e:
                    print(f"!ask** username: {user_name}")

@client.remove_command("help")
#---------------------------------------------         error CommandNotFound   -----------------------------------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore the error silently

    # Handle other types of errors if needed
    print(f"Error: {error}")



client.run(TOKEN)


