import discord
from database.db_operations import save_repeat_days_to_database
from config import bot



class DaysToRepeatView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.days = []

    @discord.ui.button(label="Monday", style=discord.ButtonStyle.blurple)
    async def monday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(1)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Tuesday", style=discord.ButtonStyle.blurple)
    async def tuesday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(2)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Wednesday", style=discord.ButtonStyle.blurple)
    async def wednesday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(3)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Thursday", style=discord.ButtonStyle.blurple)
    async def thursday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(4)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Friday", style=discord.ButtonStyle.blurple)
    async def friday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(5)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Saturday", style=discord.ButtonStyle.blurple)
    async def saturday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(6)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Sunday", style=discord.ButtonStyle.blurple)
    async def sunday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(0)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Reset All", style=discord.ButtonStyle.red)
    async def reset_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.clear()
        for child in self.children:
            if isinstance(child, discord.ui.Button) and child.label != "Reset All":
                child.disabled = False
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Send", style=discord.ButtonStyle.success)
    async def send(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel_id = 1198117804130435092
        channel = bot.get_channel(channel_id)
        save_repeat_days_to_database(self.days)
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)
        await channel.send(f"Task created successfully.")