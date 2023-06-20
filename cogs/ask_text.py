import discord
from discord import app_commands
from discord.ext import commands
from core.pageview import PageView
from bardapi import ChatBard
import asyncio
import langid

#-----------------------------
chat = ChatBard()

language_dict = {}
def detect_language(text):
    langid_result = langid.classify(text)
    excluded_languages = ["fa", "ug"]
    if langid_result[0] in excluded_languages:
        return "ar"  # Set the language to Arabic instead
    else:
        return langid_result[0]

class MyCog1(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(name="ask", description="Ask me a question.")
  async def ask(self, interaction: discord.Interaction, your_question: str):
    user_id = interaction.user.id
    user_name = interaction.user.name
    pass_question = f"**{user_name}**: {your_question}"
    await interaction.response.defer(thinking=True)
        # Detect the language
    new_language =  detect_language(your_question)
    if user_id in language_dict and new_language != language_dict[user_id]:
        response = await asyncio.to_thread(chat.start, user_id, pass_question, new_language, reset="reset")    
    else:
        response = await asyncio.to_thread(chat.start, user_id, pass_question, new_language)
    language_dict[user_id] = new_language 

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
        print(f"Guild: {guild.name},   username: {user_name}\n-----------------------------")
    except Exception as e:
        print(f"username: {user_name}\n-----------------------------")


  @app_commands.command(name="language", description='Start a new conversation in a specific language')
  @app_commands.choices(language=[
    app_commands.Choice(name='English', value="en"),
    app_commands.Choice(name='Arabic', value='ar'),
    app_commands.Choice(name='Japanese', value="ja"),
    app_commands.Choice(name='German', value="ge"),
    app_commands.Choice(name='Italian', value="it"),
    app_commands.Choice(name='Spanish', value="sp"),
    app_commands.Choice(name='Korean', value="ko"),
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
  async def language(self,interaction: discord.Interaction, language: app_commands.Choice[str], your_question: str):
    member = interaction.user
    user_id = member.id
    user_name = interaction.user.name
    await interaction.response.defer(thinking=True)
    pass_question = f"**{user_name}**: {your_question}"
    new_language =  detect_language(your_question)
    if user_id in language_dict and new_language != language_dict[user_id]:
        response = await asyncio.to_thread(chat.start, user_id, pass_question, new_language, reset="reset")    
    else:
        response = await asyncio.to_thread(chat.start, user_id, pass_question, new_language)
    language_dict[user_id] = new_language 

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
        print(f"Guild: {guild.name},   username: {user_name}\n-----------------------------")
    except Exception as e:
        print(f"username: {user_name}\n-----------------------------")



  @commands.command(name='ask', help='Ask me a question.')
  async def ask_question(self, ctx, *, your_question):
    user_id = ctx.author.id
    user_name = ctx.author.name
    pass_question = f"**{user_name}**: {your_question}"
    await ctx.defer()
         # Detect the language
    new_language =  detect_language(your_question)
    if user_id in language_dict and new_language != language_dict[user_id]:
        response = await asyncio.to_thread(chat.start, user_id, pass_question, new_language, reset="reset")    
    else:
        response = await asyncio.to_thread(chat.start, user_id, pass_question, new_language)
    language_dict[user_id] = new_language 

    embeds = []
    if len(response) > 2000:
        texts = []
        for i in range(0, len(response), 2000):
            texts.append(response[i:i+2000])
        for text in texts:
            your_question = your_question[:230]
            embed = discord.Embed(title=f""">   ``{your_question}``""",description=f"{text}",color=discord.Color.dark_gold())
            embed.set_author(name="OAN",
            icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
            embeds.append(embed)
        view = PageView(embeds)
        await ctx.reply(embed=view.initial(), view=view)
    else:
        your_question = your_question[:230]
        embed = discord.Embed(title=f""">   ``{your_question}``""",description=f"{response}",color=discord.Color.dark_gold())
        embed.set_author(name="OAN",
        icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
        embed.set_footer(text=f'{user_name}', icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    try:
        guild = ctx.guild
        print(f"!ask** Guild: {guild.name},   username: {user_name}\n-----------------------------")
    except Exception as e:
        print(f"!ask** username: {user_name}\n-----------------------------")

        
        
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog1(bot))