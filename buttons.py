import discord
from database.db_operations import save_repeat_days_to_database
from config import bot, CHANNEL_ID



class DaysToRepeatView(discord.ui.View):
    BLURPLE_STYLE = discord.ButtonStyle.blurple
    RED_STYLE = discord.ButtonStyle.red
    SUCCESS_STYLE = discord.ButtonStyle.success
    def __init__(self) -> None:
        super().__init__()
        self.days = []

    @discord.ui.button(label="Monday", style=BLURPLE_STYLE)
    async def monday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(1)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Tuesday", style=BLURPLE_STYLE)
    async def tuesday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(2)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Wednesday", style=BLURPLE_STYLE)
    async def wednesday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(3)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Thursday", style=BLURPLE_STYLE)
    async def thursday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(4)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Friday", style=BLURPLE_STYLE)
    async def friday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(5)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Saturday", style=BLURPLE_STYLE)
    async def saturday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(6)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Sunday", style=BLURPLE_STYLE)
    async def sunday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(0)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Reset All", style=RED_STYLE)
    async def reset_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.clear()
        for child in self.children:
            if isinstance(child, discord.ui.Button) and child.label != "Reset All":
                child.disabled = False
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Send", style=SUCCESS_STYLE)
    async def send(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = bot.get_channel(CHANNEL_ID)
        save_repeat_days_to_database(self.days)
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)
        await channel.send(f"Task created successfully.")