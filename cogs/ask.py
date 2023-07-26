import discord
from discord.ext import commands
from discord import app_commands
from core.pageview import PageView
from bardapi import ChatBard
import asyncio
# from core.tts import tts_audio
from core.whisper import transcribe_audio
import os
import openpyxl
from googletrans import Translator

language_dict = {}
chat = ChatBard()

def detect_language(text):
    translator = Translator()
    result = translator.detect(text)
    detected_language = result.lang
    excluded_languages = ["fa","sd"]
    excluded_languages1 = ["pt"]

    if detected_language in excluded_languages:
        return "ar"  # Set the language to Arabic instead
    
    elif detected_language in excluded_languages1:
        return "en" 
    else:
        return detected_language

class MyCog1(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    @app_commands.command(name="reset", description="Creates a new chat")
    async def reset_conversation(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_name = interaction.user.name
        pass_question = f"**{user_name}**: Hello "
        await interaction.response.defer(thinking=True)
            # Detect the language
        new_language =  'en'
        response = await asyncio.to_thread(chat.start, user_id, pass_question, reset="reset")    
        # language_dict[user_id] = new_language 
        embed = discord.Embed(title=f""">   ``reset_conversation``""",  
                              description="New chat has been open successfully"
                              ,color=discord.Color.green())
        embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
        embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
        await interaction.followup.send(embed=embed)
        try:    
            guild = interaction.guild   
            print(f"Guild: {guild.name},   username: {user_name} has been reset conversation\n-----------------------------")
        except Exception as e:
            print(f"username: {user_name}     has been reset conversation\n-----------------------------")

    @app_commands.command(name="ask", description="Ask me a question.")
    async def ask(self, interaction: discord.Interaction, your_question: str):
        user_id = interaction.user.id
        user_name = interaction.user.name
        pass_question = f"**{user_name}**: {your_question}"
        await interaction.response.defer(thinking=True)
        response = await asyncio.to_thread(chat.start, user_id, pass_question)

        embeds = []
        if len(response[0]) > 2500 and len(response) == 1:
            response = response[0]
            texts = []
            for i in range(0, len(response), 2500):
                texts.append(response[i:i+2500])
            for text in texts:
                your_question = your_question[:230]
                embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{text}", color=discord.Color.dark_gold())
                embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                embeds.append(embed)
            view = PageView(embeds)
            await interaction.followup.send(embed=view.initial(), view=view)
        elif len(response) != 1:
            for image in response:                    
                if str(image).startswith("http"):
                    embed = discord.Embed()
                    embed.set_author(name="OAN",
                    icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    embed.set_image(url=image)
                    embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
                    embeds.append(embed)
                else:
                    your_question = your_question[:230]
                    embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{image}", color=discord.Color.dark_gold())
                    embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    embeds.append(embed)
            view = PageView(embeds)
            await interaction.followup.send(embed=view.initial(), view=view)

        else:
            response = response[0]
            your_question = your_question[:230]
            embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{response}", color=discord.Color.dark_gold())
            embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
            embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
        
        try:    
            guild = interaction.guild   
            print(f"Guild: {guild.name},   username: {user_name}      \n-----------------------------")
        except Exception as e:
            print(f"username: {user_name}      \n-----------------------------")


    @commands.command(name='ask', help='Ask me a question.')
    async def ask_cmd(self, ctx, *, your_question):
        user_id = ctx.author.id
        user_name = ctx.author.name
        pass_question = f"**{user_name}**: {your_question}"
        await ctx.defer()
            # Detect the language
        # new_language =  detect_language(your_question)

        response = await asyncio.to_thread(chat.start, user_id, pass_question)
        # language_dict[user_id] = new_language 

        embeds = []

        if len(response[0]) > 2500 and len(response) == 1:
            response = response[0]
            texts = []
            for i in range(0, len(response), 2500):
                texts.append(response[i:i+2500])
            for text in texts:
                your_question = your_question[:230]
                embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{text}", color=discord.Color.dark_gold())
                embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                embeds.append(embed)
            view = PageView(embeds)
            await ctx.reply(embed=view.initial(), view=view)
        elif len(response) != 1:
            for image in response:                    
                if str(image).startswith("http"):
                    embed = discord.Embed()
                    embed.set_author(name="OAN",
                    icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    embed.set_image(url=image)
                    embed.set_footer(text=f'{user_name}', icon_url=ctx.author.avatar.url)
                    embeds.append(embed)
                else:
                    your_question = your_question[:230]
                    embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{image}", color=discord.Color.dark_gold())
                    embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    embeds.append(embed)
            view = PageView(embeds)
            await ctx.reply(embed=view.initial(), view=view)

        else:
            response = response[0]
            your_question = your_question[:230]
            embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{response}", color=discord.Color.dark_gold())
            embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
            embed.set_footer(text=f'{user_name}', icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)

        try:
            guild = ctx.guild
            print(f"!ask** Guild: {guild.name},   username: {user_name}      \n-----------------------------")
        except Exception as e:
            print(f"!ask** username: {user_name}      \n-----------------------------")
#---------------------------------------------------------------------------------------------------------------------

    @app_commands.command(name="ask_about_image", description="Upload image with question using OCR and provides answer based on the image content.")
    async def ask_about_image(self, interaction: discord.Interaction, image: discord.Attachment, your_question: str = None):
        await interaction.response.defer(thinking=True)
        user_name = interaction.user.name
        user_id = str(interaction.user.id)
        DOWNLOAD_DIR = os.path.join("image_files", user_id)
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        #error
        if not image.content_type.startswith('image'):
            embed = discord.Embed(
                title="Invalid File",
                description="Please send a image file.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
            return
        else:
            DOWNLOAD_DIR = os.path.join("image_files", user_id)

            if not os.path.exists(DOWNLOAD_DIR):
                os.makedirs(DOWNLOAD_DIR)
         
            filename = os.path.join(DOWNLOAD_DIR, image.filename)

            await image.save(filename)
            
            response = await asyncio.to_thread(chat.start, int(user_id),question = your_question,image = filename)
            if your_question == None:
                your_question  = "What is in the image?"

            embeds = []
            if len(response[0]) > 2500 and len(response) == 2:
                response = response[0]
                texts = []
                for i in range(0, len(response), 2500):
                    texts.append(response[i:i+2500])
                for text in texts:
                    your_question = your_question[:230]
                    embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{text}", color=discord.Color.dark_gold())
                    embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    embeds.append(embed)
                view = PageView(embeds)
                await interaction.followup.send(embed=view.initial(), view=view)
            elif len(response) != 2:
                for image in response:                    
                    if str(image).startswith("http"):
                        embed = discord.Embed()
                        embed.set_author(name="OAN",
                        icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                        embed.set_image(url=image)
                        embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
                        embeds.append(embed)
                    else:
                        your_question = your_question[:230]
                        embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{image}", color=discord.Color.dark_gold())
                        embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                        embeds.append(embed)
                view = PageView(embeds)
                await interaction.followup.send(embed=view.initial(), view=view)

            else:
                response = response[0]
                your_question = your_question[:230]
                embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{response}", color=discord.Color.dark_gold())
                embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
                await interaction.followup.send(embed=embed)
            
        try:    
            guild = interaction.guild   
            print(f"Guild: {guild.name},   username: {user_name}  used Ask about Image")
        except Exception as e:
            print(f"username: {user_name}    used Ask about Image \n-----------------------------")
#----------------------------------------------------------------------
    @app_commands.command(name='voice', description='Communicate with the bot using Record')
    async def ask_question(self, interaction: discord.Interaction, voice_record: discord.Attachment):
        user_name = interaction.user.name
        user_id = str(interaction.user.id)
        await interaction.response.defer(thinking=True)

        DOWNLOAD_DIR = os.path.join("audio_files", user_id)
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        filename = os.path.join(DOWNLOAD_DIR, voice_record.filename)
        await voice_record.save(filename)
        #error
        if not voice_record.content_type.startswith('audio'):
            embed = discord.Embed(
                title="Invalid File",
                description="Please send a voice record.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
            return

        your_question, language = transcribe_audio(filename)
        pass_question = f"**{user_name}**: {your_question}"
    # Detect the language

        response = await asyncio.to_thread(chat.start, int(user_id), pass_question, language)
        language_dict[int(user_id)] = language 

        # if "en" in language or "ja" in language and len(response) < 2500:
        #     your_question = your_question[:230]
        #     output_path = f"audio_files/{user_id}/output.wav"
        #     tts_audio(response[0], output_path, language)

        #     if os.path.exists(output_path):
        #         embed = discord.Embed(
        #             title=f""">   ``{your_question}``""",
        #             description=f"{response}",
        #             color=discord.Color.dark_gold()
        #         )
        #         embed.set_author(
        #             name="OAN",
        #             icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png"
        #         )
        #         embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
        #         await interaction.followup.send(embed=embed, file=discord.File(output_path, filename="output.wav"))
        #         return

        embeds = []

        if len(response[0]) > 2500 and len(response) == 1:
            response = response[0]
            texts = []
            for i in range(0, len(response), 2500):
                texts.append(response[i:i+2500])
            for text in texts:
                your_question = your_question[:230]
                embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{text}", color=discord.Color.dark_gold())
                embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                embeds.append(embed)
            view = PageView(embeds)
            await interaction.followup.send(embed=view.initial(), view=view)
        elif len(response) != 1:
            for image in response:                    
                if str(image).startswith("http"):
                    embed = discord.Embed()
                    embed.set_author(name="OAN",
                    icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    embed.set_image(url=image)
                    embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
                    embeds.append(embed)
                else:
                    your_question = your_question[:230]
                    embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{image}", color=discord.Color.dark_gold())
                    embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    embeds.append(embed)
            view = PageView(embeds)
            await interaction.followup.send(embed=view.initial(), view=view)

        else:
            response = response[0]
            your_question = your_question[:230]
            embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{response}", color=discord.Color.dark_gold())
            embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
            embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)

        try:    
            guild = interaction.guild   
            print(f"Guild: {guild.name},   username: {user_name}  used Voice ")
        except Exception as e:
            print(f"username: {user_name}    used Voice \n-----------------------------")

#----------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore messages sent by the bot itself

        sheet_path = os.path.join("core", "guild.xlsx")
        wb = openpyxl.load_workbook(sheet_path)
        sheet = wb['Sheet1']
        channel_list = [str(cell.value) for cell in sheet['B'] if cell.value]

        if str(message.channel.id) not in channel_list and not isinstance(message.channel, discord.DMChannel):
            return  # Exit if the guild is not in the channel_list and not a DM with the bot
        
        if message.content.startswith(":") or message.content.startswith("<") or message.content.startswith("!"):
            return  # Exit if the message start with ":"


        if len(message.attachments) > 0:
            for attachment in message.attachments:
                if attachment.content_type.startswith('audio'):
                    user_name = message.author.name
                    user_id = str(message.author.id)
                    DOWNLOAD_DIR = os.path.join("audio_files", user_id)

                    if not os.path.exists(DOWNLOAD_DIR):
                        os.makedirs(DOWNLOAD_DIR)

                    filename = os.path.join(DOWNLOAD_DIR, attachment.filename)
                    await attachment.save(filename)

                    your_question, language = transcribe_audio(filename)
                    pass_question = f"**{user_name}**: {your_question}"

                    response = await asyncio.to_thread(chat.start, int(user_id), pass_question, language)
                    language_dict[int(user_id)] = language

                    # if "en" in language or "ja" in language and len(response) < 2500:
                    #     output_path = f"audio_files/{user_id}/output.wav"
                    #     tts_audio(response[0], output_path, language)

                    #     if os.path.exists(output_path):
                    #         your_question = your_question[:230]
                    #         embed = discord.Embed(title=f""">   ``{your_question}``""",
                    #                             description=f"{response}",
                    #                             color=discord.Color.dark_gold())
                    #         embed.set_author(name="OAN",
                    #                         icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    #         embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)

                    #         await message.reply(embed=embed, file=discord.File(output_path, filename="output.wav"))
                    #         return

                    embeds = []
                    if len(response[0]) > 2500 and len(response) == 1:
                        response = response[0]
                        texts = []
                        for i in range(0, len(response), 2500):
                            texts.append(response[i:i+2500])
                        for text in texts:
                            your_question = your_question[:230]
                            embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{text}", color=discord.Color.dark_gold())
                            embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                            embeds.append(embed)
                        view = PageView(embeds)
                        await message.reply(embed=view.initial(), view=view)
                    elif len(response) != 1:
                        for image in response:                    
                            if str(image).startswith("http"):
                                embed = discord.Embed()
                                embed.set_author(name="OAN",
                                icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                                embed.set_image(url=image)
                                embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)
                                embeds.append(embed)
                            else:
                                your_question = your_question[:230]
                                embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{image}", color=discord.Color.dark_gold())
                                embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                                embeds.append(embed)
                        view = PageView(embeds)
                        await message.reply(embed=view.initial(), view=view)

                    else:
                        response = response[0]
                        your_question = your_question[:230]
                        embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{response}", color=discord.Color.dark_gold())
                        embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                        embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)
                        await message.reply(embed=embed)
                        
                elif attachment.content_type.startswith(('video', 'gif')):
                    return

                elif attachment.content_type.startswith('image'):
                    your_question  = "What is in the image?"
                    user_name = message.author.name
                    user_id = str(message.author.id)
                    DOWNLOAD_DIR = os.path.join("image_files", user_id)

                    if not os.path.exists(DOWNLOAD_DIR):
                        os.makedirs(DOWNLOAD_DIR)
                    filename = os.path.join(DOWNLOAD_DIR, attachment.filename)
                    await attachment.save(filename)
                    
                    response = await asyncio.to_thread(chat.start, int(user_id), image = filename)

                    embeds = []
                    if len(response[0]) > 2500 and len(response) == 2:
                        response = response[0]
                        texts = []
                        for i in range(0, len(response), 2500):
                            texts.append(response[i:i+2500])
                        for text in texts:
                            your_question = your_question[:230]
                            embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{text}", color=discord.Color.dark_gold())
                            embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                            embeds.append(embed)
                        view = PageView(embeds)
                        await message.reply(embed=view.initial(), view=view)
                    elif len(response) != 2:
                        for image in response:                    
                            if str(image).startswith("http"):
                                embed = discord.Embed()
                                embed.set_author(name="OAN",
                                icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                                embed.set_image(url=image)
                                embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)
                                embeds.append(embed)
                            else:
                                your_question = your_question[:230]
                                embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{image}", color=discord.Color.dark_gold())
                                embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                                embeds.append(embed)
                        view = PageView(embeds)
                        await message.reply(embed=view.initial(), view=view)

                    else:
                        response = response[0]
                        your_question = your_question[:230]
                        embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{response}", color=discord.Color.dark_gold())
                        embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                        embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)
                        await message.reply(embed=embed)
                    try:
                        guild = message.guild
                        print(f"______ Guild: {guild.name},   username: {user_name} used Ask about Image    \n-----------------------------")
                    except AttributeError as e:
                        print(f"______ name: {message.author.name}       used Ask about Image \n----------------------------- ")
                    except Exception as e:
                        print(f"_____ username: {message.author.name}      used Ask about Image \n-----------------------------")
                    return
 

        else:
            user_id = message.author.id
            user_name = message.author.name
            pass_question = f"**{user_name}**: {message.content}"
            your_question = message.content
            # new_language = detect_language(message.content)
            response = await asyncio.to_thread(chat.start, user_id, pass_question)
            # language_dict[user_id] = new_language
            embeds = []
            if len(response[0]) > 2500 and len(response) == 1:
                response = response[0]
                texts = []
                for i in range(0, len(response), 2500):
                    texts.append(response[i:i+2500])
                for text in texts:
                    your_question = your_question[:230]
                    embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{text}", color=discord.Color.dark_gold())
                    embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    embeds.append(embed)
                view = PageView(embeds)
                await message.reply(embed=view.initial(), view=view)
            elif len(response) != 1:
                for image in response:                    
                    if str(image).startswith("http"):
                        embed = discord.Embed()
                        embed.set_author(name="OAN",
                        icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                        embed.set_image(url=image)
                        embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)
                        embeds.append(embed)
                    else:
                        your_question = your_question[:230]
                        embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{image}", color=discord.Color.dark_gold())
                        embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                        embeds.append(embed)
                view = PageView(embeds)
                await message.reply(embed=view.initial(), view=view)

            else:
                your_question = your_question[:230]
                response = response[0]
                embed = discord.Embed(title=f""">   ``{your_question}``""", description=f"{response}", color=discord.Color.dark_gold())
                embed.set_author(name="OAN", icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)
                await message.reply(embed=embed)

        try:
            guild = message.guild
            print(f"______ Guild: {guild.name},   username: {user_name}      \n-----------------------------")
        except AttributeError as e:
            print(f"______ name: {message.author.name}        \n----------------------------- ")
        except Exception as e:
            print(f"_____ username: {message.author.name}      \n-----------------------------")

        await self.bot.process_commands(message)


        
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog1(bot))