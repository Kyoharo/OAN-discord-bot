import discord
from discord import app_commands
from discord.ext import commands
import openpyxl
from openpyxl.styles import Alignment, Border, Side
import os

class MyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setchannel", description="To create a channel to be the main channel where users can chat with the chatbot")
    async def setchannel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        channel_id = str(channel.id)  # Convert to string
        user_name = interaction.user.name
        guild = str(interaction.guild.id)  # Convert to string
        await interaction.response.defer(thinking=True)

        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="Invalid user",
                description="This command requires the ``Administrator`` permission",
                color=discord.Color.red()
            )
            embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)
            return

        else:
            sheet_path = os.path.join("core", "guild.xlsx")
            wb = openpyxl.load_workbook(sheet_path)
            sheet = wb['Sheet1']
            max_rows = sheet.max_row + 1
            gg = sheet.cell(2, 1).value
            is_registered = False  # Flag variable
            
            for row in range(2, max_rows):  # Start from row 2
                if guild == str(sheet.cell(row, 1).value):
                    if channel_id == str(sheet.cell(row, 2).value):
                        is_registered = True
                        break  # Channel is already registered, break the loop
                    else:
                        sheet.cell(row, 2).value = channel_id
                        sheet.cell(row, 4).value = channel.name
                        is_registered = True
                        break
            
            if is_registered:
                embed = discord.Embed(
                    title=f"Channel updated: ``{channel.name}``",
                    description="This channel has been updated in the registration",
                    color=discord.Color.purple()
                )
                embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
                await interaction.followup.send(embed=embed)
                wb.save(sheet_path)
                return
            
            alignment = Alignment(horizontal='center', vertical='center')
            cell = sheet.cell(max_rows, 1)
            cell.alignment = alignment
            # Apply borders and set color to gray
            border = Border(
                left=Side(border_style='thin', color='FF808080'),
                right=Side(border_style='thin', color='FF808080'),
                top=Side(border_style='thin', color='FF808080'),
                bottom=Side(border_style='thin', color='FF808080')
            )
            cell.border = border
            cell.value = guild
            #---------------------
            #channel_id
            cell = sheet.cell(max_rows, 2)
            cell.alignment = alignment
            cell.border = border
            cell.value = channel_id
            #---------------------
            #guild name
            cell = sheet.cell(max_rows, 3)
            cell.alignment = alignment
            cell.border = border
            cell.value = interaction.guild.name
            #---------------------
            #channel name
            cell = sheet.cell(max_rows, 4)
            cell.alignment = alignment
            cell.border = border
            cell.value = channel.name
            wb.save(sheet_path)
            embed = discord.Embed(
                title=f"OAN default channel is now ``{channel.name}``",
                description="The channel has been set successfully",
                color=discord.Color.green()
            )
            embed.set_footer(text=f'{user_name}', icon_url=interaction.user.avatar.url)
            await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyCog(bot))
