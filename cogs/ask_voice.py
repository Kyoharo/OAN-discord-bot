import discord
from discord.ext import commands
from discord import app_commands

from core.pageview import PageView
from bardapi import ChatBard
import asyncio
import langid
from core.tts import tts_audio
from core.whisper import transcribe_audio
import os


language_dict = {}

#-----------------------------
chat = ChatBard()

def detect_language(text):
    langid_result = langid.classify(text)
    excluded_languages = ["fa", "ug"]
    if langid_result[0] in excluded_languages:
        return "ar"  # Set the language to Arabic instead
    else:
        return langid_result[0]
    

class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

#---------------------------------------------         slash voice       -----------------------------------------------------------------
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
        if int(user_id) in language_dict and language != language_dict[int(user_id)]:
            response = await asyncio.to_thread(chat.start, int(user_id), pass_question, language, reset="reset")    
        else:
            response = await asyncio.to_thread(chat.start, int(user_id), pass_question, language)
        language_dict[int(user_id)] = language 

        if "en" in language or "ja" in language and len(response) < 2000:
            your_question = your_question[:230]
            output_path = f"audio_files/{user_id}/output.wav"
            tts_audio(response, output_path, language)

            if os.path.exists(output_path):
                embed = discord.Embed(
                    title=f""">   ``{your_question}``""",
                    description=f"{response}",
                    color=discord.Color.dark_gold()
                )
                embed.set_author(
                    name="OAN",
                    icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png"
                )
                embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                await interaction.followup.send(embed=embed, file=discord.File(output_path, filename="output.wav"))
                return

        embeds = []
        if len(response) > 2000:
            texts = [response[i:i + 2000] for i in range(0, len(response), 2000)]
            for text in texts:
                your_question = your_question[:230]
                embed = discord.Embed(
                    title=f""">   ``{your_question}``""",
                    description=f"{text}",
                    color=discord.Color.dark_gold()
                )
                embed.set_author(
                    name="OAN",
                    icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png"
                )
                embeds.append(embed)
            view = PageView(embeds)
            await interaction.followup.send(embed=view.initial(), view=view)
        else:
            your_question = your_question[:230]
            embed = discord.Embed(
                title=f""">   ``{your_question}``""",
                description=f"{response}",
                color=discord.Color.dark_gold()
            )
            embed.set_author(
                name="OAN",
                icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png"
            )
            embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)


#---------------------------------------------         on_message       -----------------------------------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            return  # Ignore messages in guilds
        if message.author == self.bot.user:
         return  # Ignore messages sent by the bot itself

        if isinstance(message.channel, discord.DMChannel) and message.author != self.bot.user:
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
                        # Detect the language
                        if int(user_id) in language_dict and language != language_dict[int(user_id)]:
                            response = await asyncio.to_thread(chat.start, int(user_id), pass_question, language, reset="reset")
                        else:
                            response = await asyncio.to_thread(chat.start, int(user_id), pass_question, language)
                        language_dict[int(user_id)] = language

                        # Convert the response to speech
                        if "en" in language or "ja" in language and len(response) < 2000:
                            output_path = f"audio_files/{user_id}/output.wav"
                            tts_audio(response, output_path, language)
                            if os.path.exists(output_path):
                                your_question = your_question[:230]
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
                            texts = [response[i:i + 2000] for i in range(0, len(response), 2000)]
                            for text in texts:
                                your_question = your_question[:230]
                                embed = discord.Embed(title=f""">   ``{your_question}``""",
                                                      description=f"{text}",
                                                      color=discord.Color.dark_gold())
                                embed.set_author(name="OAN",
                                                 icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                                embeds.append(embed)
                            view = PageView(embeds)
                            await message.channel.send(embed=view.initial(), view=view)
                        else:
                            your_question = your_question[:230]
                            embed = discord.Embed(title=f""">   ``{your_question}``""",
                                                  description=f"{response}",
                                                  color=discord.Color.dark_gold())
                            embed.set_author(name="OAN",
                                             icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                            embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)
                            await message.channel.send(embed=embed)

            else:
                user_id = message.author.id
                user_name = message.author.name
                pass_question = f"**{user_name}**: {message.content}"
                # Detect the language
                new_language = detect_language(message.content)
                if user_id in language_dict and new_language != language_dict[user_id]:
                    response = await asyncio.to_thread(chat.start, user_id, pass_question, new_language, reset="reset")
                else:
                    response = await asyncio.to_thread(chat.start, user_id, pass_question, new_language)
                language_dict[user_id] = new_language
                embeds = []
                if len(response) > 2000:
                    texts = []
                    for i in range(0, len(response), 2000):
                        texts.append(response[i:i + 2000])
                    for text in texts:
                        your_question = message.content[:230]
                        embed = discord.Embed(title=f""">   ``{your_question}``""",
                                              description=f"{text}",
                                              color=discord.Color.dark_gold())
                        embed.set_author(name="OAN",
                                         icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                        embeds.append(embed)
                    view = PageView(embeds)
                    await message.reply(embed=view.initial(), view=view)
                else:
                    your_question = message.content[:230]
                    embed = discord.Embed(title=f""">   ``{your_question}``""",
                                          description=f"{response}",
                                          color=discord.Color.dark_gold())
                    embed.set_author(name="OAN",
                                     icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
                    embed.set_footer(text=f'{user_name}', icon_url=message.author.avatar.url)
                    await message.reply(embed=embed)

            try:
                guild = message.guild
                print(f"!ask** Guild: {guild.name},   username: {user_name}\n-----------------------------")
            except Exception as e:
                print(f"!ask** username: {user_name}\n-----------------------------")

        await self.bot.process_commands(message)
    


        
        
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog(bot))