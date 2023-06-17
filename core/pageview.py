import discord
from typing import List

class PageView(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed]) -> None:
        super().__init__(timeout=864000)
        self._embeds = embeds
        self._len = len(embeds)
        self._current_page = 1

    async def update_buttons(self, interaction: discord.Interaction) -> None:
        embed = self._embeds[self._current_page - 1]
        embed.set_footer(text=f"Pages: {self._current_page}/{self._len}", icon_url=interaction.user.avatar.url)
        await interaction.message.edit(embed=embed)

    @discord.ui.button(emoji='⏮️')
    async def previous(self, interaction: discord.Interaction, _):
        if self._current_page == 1:
            return
        self._current_page -= 1
        embed = self._embeds[self._current_page - 1]
        await interaction.response.edit_message(embed=embed)
        await self.update_buttons(interaction)

    @discord.ui.button(emoji='⏭️')
    async def next(self, interaction: discord.Interaction, _):
        if self._current_page == self._len:
            return
        self._current_page += 1
        embed = self._embeds[self._current_page - 1]
        await interaction.response.edit_message(embed=embed)
        await self.update_buttons(interaction)

    def initial(self) -> discord.Embed:
        return self._embeds[0]