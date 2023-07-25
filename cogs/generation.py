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
import base64

def query1(payload):
    API_URL = "https://api-inference.huggingface.co/models/gsdf/Counterfeit-V2.5"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        return None

def query2(payload):
    API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        return None




def query3(payload):
    API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        return None


def query4(payload):
    API_URL = "https://api-inference.huggingface.co/models/stablediffusionapi/anything-v5"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        return None





def upload_image(image_content):
    upload_url = "https://api.imgbb.com/1/upload"
    encoded_image = base64.b64encode(image_content).decode("utf-8")
    payload = {
        "key": "15125cfd3e76996b00941f181a5711b1",
        "image": encoded_image
    }
    response = requests.post(upload_url, payload)
    json_response = response.json()
    if json_response["status"] == 200:
        return json_response["data"]["url"]
    else:
        return None

def upload_image2(image_bytes):
    client_id = "7725fb46bd3966b"
    headers = {"Authorization": f"Client-ID {client_id}"}
    url = "https://api.imgur.com/3/upload"
    response = requests.post(url, headers=headers, files={"image": image_bytes})
    data = response.json()
    if response.status_code == 200 and data["success"]:
        image_link = data["data"]["link"]
        print("used upload_image2")
        return image_link
    else:
        print("Image upload failed.")
        return None

def get_image_link(query_text, model):
    if model == 1:
        image_bytes = query1({"inputs": query_text})
        if image_bytes == None:
            image_bytes = query2({"inputs": query_text})
            if image_bytes == None:
                image_bytes = query3({"inputs": query_text})  
                if image_bytes == None:
                   image_bytes = query4({"inputs": query_text})    

    elif model == 2:
        image_bytes = query2({"inputs": query_text})
        if image_bytes == None:
            image_bytes = query3({"inputs": query_text})
            if image_bytes == None:
                image_bytes = query4({"inputs": query_text})  
                if image_bytes == None:
                   image_bytes = query1({"inputs": query_text})  

    elif model == 3:
        image_bytes = query3({"inputs": query_text})
        if image_bytes == None:
            image_bytes = query4({"inputs": query_text})
            if image_bytes == None:
                image_bytes = query1({"inputs": query_text})  
                if image_bytes == None:
                   image_bytes = query2({"inputs": query_text})  
    elif model == 4:
        image_bytes = query4({"inputs": query_text})
        if image_bytes == None:
            image_bytes = query1({"inputs": query_text})
            if image_bytes == None:
                image_bytes = query2({"inputs": query_text})  
                if image_bytes == None:
                   image_bytes = query3({"inputs": query_text})  
    image_link = upload_image(image_bytes)
    if image_link is None or not image_link.startswith("http"):
        image_link = upload_image2(image_bytes)

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
    async def imagine(self, interaction: discord.Interaction, prompt: str, models: app_commands.Choice[int] = None):
        await interaction.response.defer(thinking=True)
        
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
            "https://media.discordapp.net/attachments/1085541383563124858/1121957069604532244/Anime_Cry_Sticker_-_Anime_Cry_Sad_-_Discover__Share_GIFs.gif",
            "https://media.discordapp.net/attachments/692123394971533393/1122215837806370940/e5649b4b6914beeb679ff15ea74b7aec.gif",
            "https://media.discordapp.net/attachments/692123394971533393/1122215838204837898/21740ae095edd3fc474b6d9c14d25a0f.gif",
            "https://media.discordapp.net/attachments/692123394971533393/1122215838590705805/0078b8dd6501402668ef94bbb99eec83.gif",
            "https://media.discordapp.net/attachments/692123394971533393/1122215838955618456/4905109f43ae6aad5d3c2fd417d9dde2.gif"
        ]

        try:

            embed = discord.Embed()
            embed.set_author(name="OAN",
            icon_url="https://cdn.discordapp.com/attachments/1085541383563124858/1113276038634541156/neka_xp2.png")
            embed.set_image(url=random.choice(loading_images))
            embed.set_footer(text=f"Loading...! Generating image...", icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)

            if models == None:
                response = await asyncio.to_thread(get_image_link, prompt,1)
                if response == None:
                    response = await asyncio.to_thread(get_image_link, prompt,3)
                    print("model3")
            elif models.value == 1:
                response = await asyncio.to_thread(get_image_link, prompt,1)
                if response == None:
                    response = await asyncio.to_thread(get_image_link, prompt,3)
                    print("model3")
            elif models.value == 2:
                response = await asyncio.to_thread(get_image_link, prompt,2)
                if response == None:
                    response = await asyncio.to_thread(get_image_link, prompt,4)
                    print("model4")
            elif models.value == 3:
                response = await asyncio.to_thread(get_image_link, prompt,3)
                if response == None:
                    response = await asyncio.to_thread(get_image_link, prompt,1)
                    print("model1")
            elif models.value == 4:
                response = await asyncio.to_thread(get_image_link, prompt,4)
                if response == None:
                    response = await asyncio.to_thread(get_image_link, prompt,2)
                    print("model2")



            prompt = prompt[:230]
            embed = discord.Embed(
                description=f'**[{prompt}]({response})**')
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



