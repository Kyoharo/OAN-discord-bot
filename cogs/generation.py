import discord
from discord import app_commands
from discord.ext import commands
import os
import requests
import time
import random
import asyncio
import json
import io



def query1(payload):
    API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def query2(payload):
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def query3(payload):
    API_URL = "https://api-inference.huggingface.co/models/gsdf/Counterfeit-V2.5"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def query4(payload):
    API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content



def upload_image(image_bytes):
    headers = {"Authorization": "Client-ID YOUR_CLIENT_ID"}
    url = "https://api.imgur.com/3/upload"
    response = requests.post(url, headers=headers, files={"image": image_bytes})
    data = response.json()
    if response.status_code == 200 and data["success"]:
        image_link = data["data"]["link"]
        return image_link
    else:
        print("Image upload failed.")
        return None

def get_image_link(query_text,model):
    if model == 1:
        image_bytes = query1({"inputs": query_text})
    elif model ==2:
        image_bytes = query2({"inputs": query_text})
    elif model ==3:
        image_bytes = query3({"inputs": query_text})
    elif model ==4:
        image_bytes = query4({"inputs": query_text})
    image_link = upload_image(image_bytes)
    return image_link

class Image(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="imagine", description="Turns Your Imagination Into Images Via AI")
    @app_commands.choices(models=[
    app_commands.Choice(name='Model1', value=1),
    app_commands.Choice(name='Model2', value=2),
    app_commands.Choice(name='Model3', value=3),
    app_commands.Choice(name='Model4', value=4),
    ])
    async def imagine(self, interaction: discord.Interaction, prompt: str, models: app_commands.Choice[int]):
        await interaction.response.defer(thinking=True)
        ETA = int(time.time() + 30)
        loading_images = [
            "https://media.discordapp.net/attachments/1085541383563124858/1121954059759386644/loading9.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121954060107530340/loading8.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121954060485009439/loading7.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121954060837339227/loading6.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121954061235789896/loading5.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121954062049493093/loading3.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121954062536024134/loading2.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121954062926086184/loading.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121957227994021949/13.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121957069604532244/Anime_Cry_Sticker_-_Anime_Cry_Sad_-_Discover__Share_GIFs.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121957070544060456/16d4b4d9d668fb59.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121957071018004500/Loading_Fast_GIF_-_Loading_Fast_-_Discover__Share_GIFs.gif",
            "https://media.discordapp.net/attachments/1085541383563124858/1121957069604532244/Anime_Cry_Sticker_-_Anime_Cry_Sad_-_Discover__Share_GIFs.gif"
        ]

        try:
            embed = discord.Embed(
            title=f"Loading...! Generating image... ETA: <t:{ETA}:R>")
            embed.set_author(name="OAN",
            icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
            embed.set_image(url=random.choice(loading_images))
            embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
            if models.value == 1:
                response = await asyncio.to_thread(get_image_link, prompt,1)
            elif models.value == 2:
                response = await asyncio.to_thread(get_image_link, prompt,2)
            elif models.value == 3:
                response = await asyncio.to_thread(get_image_link, prompt,3)
            elif models.value == 4:
                response = await asyncio.to_thread(get_image_link, prompt,4)


            prompt = prompt[:230]
            embed = discord.Embed(
                title=prompt)
            embed.set_author(name="OAN",
            icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
            embed.set_image(url=response)
            embed.set_footer(text=f'{interaction.user.name}', icon_url=interaction.user.avatar.url)
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            print(e)

        try:
            print(f" imagine: guild: {interaction.guild.name}   user: {interaction.user.name}\n")
        except Exception as e:
            print(f" imagine: user: {interaction.user.name}\n")




async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Image(bot))
