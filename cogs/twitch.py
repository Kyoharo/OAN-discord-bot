import requests
from dotenv import load_dotenv
import os
import openpyxl
import discord
from discord import app_commands
from discord.ext import commands
from openpyxl.styles import Alignment, Border, Side
from discord.ext import tasks
from datetime import datetime


class TwitchStreamChecker:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID_TWITCH')
        self.client_secret = os.getenv('CLIENT_SECRET_TWITCH')
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        body = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            "grant_type": 'client_credentials'
        }
        response = requests.post('https://id.twitch.tv/oauth2/token', body)
        keys = response.json()
        return keys['access_token']
    
    def is_user_exist(self, streamer_name):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self.access_token
        }
        user_data = requests.get('https://api.twitch.tv/helix/users?login=' + streamer_name, headers=headers).json()
        user_info = user_data.get('data', None)
        
        if user_info:
            user_info = user_info[0]
            return {
                'id': user_info['id'],
                'login': user_info['login'],
                'display_name': user_info['display_name'],
                'profile_image_url': user_info['profile_image_url'],
            }
        else:
            return None

    def is_streamer_live(self, streamer_name):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self.access_token
        }
        
        user_info = self.is_user_exist(streamer_name)
        
        stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)
        stream_data = stream.json()
        
        if len(stream_data['data']) == 1:
            stream_info = stream_data['data'][0]
            thumbnail_url = stream_info['thumbnail_url'].replace("{width}", "500").replace("{height}", "250")
            
            return {
                'is_live': True,
                'stream_title': stream_info['title'],
                'game_name': stream_info['game_name'],
                'viewer_count': stream_info['viewer_count'],
                'thumbnail_url': thumbnail_url,
                'started_at': stream_info['started_at'],
                'profile_image_url': user_info['profile_image_url'],
            }
        else:
            return {
                'is_live': False
            }

class twitch_cog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.twitch_checker = TwitchStreamChecker()
        self.update_stream_status.start()

    @tasks.loop(seconds=90)
    async def update_stream_status(self):
        sheet_path = os.path.join("core", "twitch_guild.xlsx")
        wb = openpyxl.load_workbook(sheet_path)
        sheet_names = wb.sheetnames
        for guild in sheet_names:
            sheet = wb[guild]
            max_rows = sheet.max_row + 1
            for row in range(2, max_rows): 
                streamer = str(sheet.cell(row, 1).value)
                stream_info = self.twitch_checker.is_streamer_live(streamer)
                if stream_info['is_live']:
                    status = str(sheet.cell(row, 2).value)
                    if status != "True":
                        channel_id = int(sheet.cell(1, 3).value)
                        message = str(sheet.cell(row, 5).value)
                        text_channel = self.bot.get_channel(channel_id)
                        embed = discord.Embed(
                            title=stream_info['stream_title'],  # Use the stream title directly as the title
                            color=0x6a95a2,
                            url=f"https://www.twitch.tv/{streamer}"  # Set the URL for the title hyperlink
                        )
                        embed.set_author(name=f"[LIVE] {streamer}", icon_url=stream_info['profile_image_url'], url=f"https://www.twitch.tv/{streamer}") 
                                        
                        width = 500
                        height = 250
                        # Modify the thumbnail_url to use the desired width and height
                        thumbnail_url = stream_info['thumbnail_url'].replace("{width}", str(width)).replace("{height}", str(height))
                        embed.set_image(url=thumbnail_url)
                        embed.add_field(name="Game", value=stream_info['game_name'])
                        embed.add_field(name="Viewer Count", value=stream_info['viewer_count'])
                        # started_at_utc = datetime.strptime(stream_info['started_at'], "%Y-%m-%dT%H:%M:%SZ")
                        #add button
                        view = discord.ui.View()
                        button = discord.ui.Button(emoji="<:Twitch:1136322224018694195>]",label=f" Twitch.com/{streamer}",url=f"https://www.twitch.tv/{streamer}")
                        view.add_item(button)
                        # Convert to the desired format
                        # started_at_local = started_at_utc.strftime("%-d/%-m/%Y %-I:%M %p")
                        embed.set_footer(text=f"OAN")

                        if str(message) == 'None':
                            regular_message = f"**{streamer} is now LIVE on Twitch @everyone**"
                        else:
                            regular_message = message

                        await text_channel.send(regular_message, embed=embed,view=view)
                        print(f"\n\n twitch {streamer} have been sended \n\n")                    
                    sheet.cell(row, 2).value = "True"
                    wb.save(sheet_path)
                else:
                    sheet.cell(row, 2).value = "False"
                    wb.save(sheet_path)

    @update_stream_status.before_loop
    async def before_update_stream_status(self):
        await self.bot.wait_until_ready()



    @app_commands.command(name="announcechannel", description="Sets the discord channel where stream announcements will be posted.")
    @app_commands.guild_only()
    async def announcechannel(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel):
        channel_id = str(channel.id)  # Convert to string
        user_name = interaction.user.name
        guild = str(interaction.guild.id)  # Convert to string
        await interaction.response.defer(thinking=True)

        if not (interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
            embed = discord.Embed(
                title="Invalid user",
                description="This command requires the ``Administrator or Manage channels`` permission",
                color=discord.Color.red()
            )
            embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
            if interaction.user.avatar:
                embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
            return

        else:
            sheet_path = os.path.join("core", "twitch_guild.xlsx")
            wb = openpyxl.load_workbook(sheet_path)
            sheet_names = wb.sheetnames
            if guild not in sheet_names:
                # Create a new worksheet with the value of guild_id
                wb.create_sheet(guild)
            sheet = wb[guild]
                #SET THE DEFUALT CHANNEL
            if sheet.cell(1, 3).value is None:
                sheet.cell(1, 3).value = channel_id
                wb.save(sheet_path)
                embed = discord.Embed(
                title=f"OAN default announcechannel is ``{channel.name}``",
                description=f"The {channel.name} has been set successfully\n Now you can add streamers by </addstreamer:1135989711253536789>",
                color=0x6a95a2
            )
                embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                if interaction.user.avatar:
                    embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                await interaction.followup.send(embed=embed)
                print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name}  has been set announcechannel\n **************************************")
                return


            elif channel_id == str(sheet.cell(1, 3).value):
                embed = discord.Embed(
                        title=f"Registration ``{channel}``",
                        description=f"**{channel}**  has already been registered",
                        color=0x6a95a2
                    )
                embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                if interaction.user.avatar:
                    embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                await interaction.followup.send(embed=embed)
                print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} has already been registered announcechannel\n **************************************")
                return
                

            else:
                sheet.cell(1, 3).value = channel_id
                wb.save(sheet_path)
                embed = discord.Embed(
                    title=f"Channel updated: ``{channel.name}``",
                    description="This channel has been updated in the registration",
                    color=0x6a95a2
                )
                embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                if interaction.user.avatar:
                    embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                await interaction.followup.send(embed=embed)
                print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} has been updated\n **************************************")
                return

    @app_commands.command(name="addstreamer", description="Adds a new streamer to list of streamers being monitored")
    @app_commands.guild_only()
    async def addstreamers(self, interaction: discord.Interaction, streamer: str, stream_message: str = None):
        try:
            user_name = interaction.user.name
            guild = str(interaction.guild.id)  # Convert to string
            await interaction.response.defer(thinking=True)

            if not (interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
                embed = discord.Embed(
                    title="Invalid user",
                    description="This command requires the ``Administrator or Manage channels`` permission",
                    color=discord.Color.red()
                )
                embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                if interaction.user.avatar:
                    embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                await interaction.followup.send(embed=embed)
                print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} has already send you don't have permistion\n **************************************")

                return

            else:
                sheet_path = os.path.join("core", "twitch_guild.xlsx")
                wb = openpyxl.load_workbook(sheet_path)
                sheet_names = wb.sheetnames
                if guild not in sheet_names:
                    embed = discord.Embed(
                        title="Invaild announcechannel",
                        description="Please use command </announcechannel:1135989711253536788> first to Set the discord channel where stream announcements will be posted.",
                        color=discord.Color.dark_orange()
                    )
                    embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                    if interaction.user.avatar:
                        embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                    await interaction.followup.send(embed=embed)
                    print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} has already send use announcements first\n **************************************")

                    return
        
                sheet = wb[guild]
                max_rows = sheet.max_row + 1
                for row in range(1, max_rows):  # Start from row 2
                    if str(streamer).lower() == str(sheet.cell(row, 1).value).lower():
                        embed = discord.Embed(
                            title=f"``{streamer}'s registration``",
                            description=f"**{streamer}**  has already been registered by {str(sheet.cell(row=row, column=4).value)}",
                            color=0x6a95a2
                        )
                        embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                        if interaction.user.avatar:
                            embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                        await interaction.followup.send(embed=embed)
                        print(f"************************************************\n guild {interaction.guild.name} has already been registered addstreamers\n **************************************")
                        sheet.cell(row, 5).value = stream_message
                        wb.save(sheet_path)
                        return
                    
                check_streamer = TwitchStreamChecker()
                if check_streamer.is_user_exist(streamer.lower()) :
                    alignment = Alignment(horizontal='center', vertical='center')
                    cell = sheet.cell(max_rows, 1)
                    cell.alignment = alignment
                    # Apply bordsers and set color to gray
                    border = Border(
                        left=Side(border_style='thin', color='FF808080'),
                        right=Side(border_style='thin', color='FF808080'),
                        top=Side(border_style='thin', color='FF808080'),
                        bottom=Side(border_style='thin', color='FF808080')
                    )
                    cell.border = border
                    #sreamer name
                    cell = sheet.cell(max_rows, 1)
                    cell.alignment = alignment
                    cell.border = border
                    cell.value = streamer
                    #status
                    cell = sheet.cell(max_rows, 2)
                    cell.alignment = alignment
                    cell.border = border
                    cell.value = "False"
                    #---------------------
                    #guild_name
                    cell = sheet.cell(max_rows, 3)
                    cell.alignment = alignment
                    cell.border = border
                    cell.value = interaction.guild.name
                    #author
                    cell = sheet.cell(max_rows, 4)
                    cell.alignment = alignment
                    cell.border = border
                    cell.value = interaction.user.name
                    #message
                    cell = sheet.cell(max_rows, 5)
                    cell.alignment = alignment
                    cell.border = border
                    cell.value = stream_message

                    wb.save(sheet_path)
                    embed = discord.Embed(
                        title=f"``{streamer}'s`` registration",
                        description=f"**{streamer}** has been set successfully",
                        color=0x6a95a2
                    )
                    embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                    if interaction.user.avatar:
                        embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                    await interaction.followup.send(embed=embed)
                    print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} has been set add streamer \n **************************************")
                    return
                else: 
                    embed = discord.Embed(
                    title=f"``{streamer}'s``  registration",
                    description=f"**{streamer}** Can't find the user in Twitch please check the name!",
                    color=discord.Color.red()
                    )
                    embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")

                    if interaction.user.avatar:
                        embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                    await interaction.followup.send(embed=embed)
                    print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} Can't find the user in Twitch \n **************************************")
                    return
        except Exception as e : 
            print(e)

    @app_commands.command(name="streamers", description="Shows a list of streamers currently being monitored.")
    @app_commands.guild_only()
    async def streamers(self, interaction: discord.Interaction):
        try:
            user_name = interaction.user.name
            guild = str(interaction.guild.id)  # Convert to string
            await interaction.response.defer(thinking=True)

            if not (interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
                embed = discord.Embed(
                    title="Invalid user",
                    description="This command requires the ``Administrator or Manage channels`` permission",
                    color=discord.Color.red()
                )
                embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                if interaction.user.avatar:
                    embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} has already send you don't have permistion\n **************************************")

                await interaction.followup.send(embed=embed)

                return

            else:
                sheet_path = os.path.join("core", "twitch_guild.xlsx")
                wb = openpyxl.load_workbook(sheet_path)
                sheet_names = wb.sheetnames
                if guild not in sheet_names:
                    embed = discord.Embed(
                        title="Invaild announcechannel",
                        description="Please use command </announcechannel:1135989711253536788> first to Sets the discord channel where stream announcements will be posted.",
                        color=discord.Color.dark_orange()
                    )
                    embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                    if interaction.user.avatar:
                        embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                    await interaction.followup.send(embed=embed)
                    print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} has already send use announcechannel\n **************************************")
                    return
        
                sheet = wb[guild]
                streamers = []
                max_rows = sheet.max_row + 1
                embed = discord.Embed(
                title=f"Streamers",
                description=f"**list of streamers currently being monitored**",
                color=0x6a95a2)
                embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458") 

                for row in range(2, max_rows): # St art from row 2
                    streamers.append(str(sheet.cell(row, 1).value))
                for streamer in streamers:
                    embed.add_field(name="Name", value=f"`{streamer}`", inline="False")
                if interaction.user.avatar:
                    embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                await interaction.followup.send(embed=embed)
                print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} has send list of streamers\n **************************************")
                return

        except Exception as e : 
            print(e)

    @app_commands.command(name="removestreamer", description="Removes streamer from the  list of streamers being monitored")
    @app_commands.guild_only()
    async def removestreamer(self, interaction: discord.Interaction, removestreamer: str):
        try:
            user_name = interaction.user.name
            guild = str(interaction.guild.id)  # Convert to string
            await interaction.response.defer(thinking=True)

            if not (interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels):
                embed = discord.Embed(
                    title="Invalid user",
                    description="This command requires the ``Administrator or Manage channels`` permission",
                    color=discord.Color.red()
                )
                embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                if interaction.user.avatar:
                    embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} has already send you don't have permistion\n **************************************")

                await interaction.followup.send(embed=embed)

                return

            else:
                sheet_path = os.path.join("core", "twitch_guild.xlsx")
                wb = openpyxl.load_workbook(sheet_path)
                sheet_names = wb.sheetnames
                if guild not in sheet_names:
                    embed = discord.Embed(
                        title="Invaild Streamer",
                        description="You have to set </announcechannel:1135989711253536788> first! ",
                        color=discord.Color.dark_orange()
                    )
                    embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")

                    if interaction.user.avatar:
                        embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                    await interaction.followup.send(embed=embed)
                    print(f"************************************************\n guild {interaction.guild.name} : {interaction.user.name} has already send use announcechannel\n **************************************")
                    return
        
                sheet = wb[guild]
                streamers = []
                max_rows = sheet.max_row + 1 
                remove_row_index = None
                for row in range(2, max_rows): # Start from row 2
                    streamer = str(sheet.cell(row, 1).value).lower()
                    streamers.append(streamer)
                    if streamer == removestreamer.lower():
                        remove_row_index = row

                # If removestreamer is found, delete the row
                if remove_row_index is not None:
                    sheet.delete_rows(remove_row_index)
                    embed = discord.Embed(
                    title=f"Remove Streamer",
                    description=f"**`{removestreamer}` has been deleted successfully**",
                    color=0x6a95a2)
                    embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                    if interaction.user.avatar:
                        embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                    await interaction.followup.send(embed=embed)
                    wb.save(sheet_path)
                    print(f"************************************************\n guild {interaction.guild.name}: {interaction.user.name} has been deleted {removestreamer}\n **************************************")
                    return
                else:
                    embed = discord.Embed(
                    title=f"Remove Streamer",
                    description=f"**`{removestreamer}` Invaild** you can know the streamers using </streamers:1135989711253536790> ",
                    color=discord.Color.dark_orange())
                    embed.set_author(name=f"OAN", icon_url="https://media.discordapp.net/attachments/1085541383563124858/1135948796006781008/-51609794436soaav8dnrc.png?width=537&height=458")
                    if interaction.user.avatar:
                        embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                    await interaction.followup.send(embed=embed)
                    print(f"************************************************\n guild {interaction.guild.name}: {interaction.user.name} has been try to delete invalid {removestreamer}\n **************************************")
                    return

        except Exception as e : 
            print(e)


                            



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(twitch_cog(bot))


