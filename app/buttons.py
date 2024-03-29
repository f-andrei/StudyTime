import discord
from database.task_operations import save_repeat_days_to_database
from utils.embed_utils import display_embed



class DaysToRepeatView(discord.ui.View):
    BLURPLE_STYLE = discord.ButtonStyle.blurple
    RED_STYLE = discord.ButtonStyle.red
    SUCCESS_STYLE = discord.ButtonStyle.success
    def __init__(self, task_data, task_id, msg_id) -> None:
        super().__init__()
        self.days = []
        self.task_data = task_data
        self.task_id = task_id
        self.msg_id = msg_id

    @discord.ui.button(label="Monday", style=BLURPLE_STYLE)
    async def monday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(0)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Tuesday", style=BLURPLE_STYLE)
    async def tuesday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(1)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Wednesday", style=BLURPLE_STYLE)
    async def wednesday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(2)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Thursday", style=BLURPLE_STYLE)
    async def thursday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(3)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Friday", style=BLURPLE_STYLE)
    async def friday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(4)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Saturday", style=BLURPLE_STYLE)
    async def saturday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(5)
        button.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Sunday", style=BLURPLE_STYLE)
    async def sunday(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.days.append(6)
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
        save_repeat_days_to_database(self.days)
        for child in self.children:
            child.disabled = True

        await interaction.response.edit_message(view=self)
        await interaction.followup.delete_message(self.msg_id)
        task_data = self.task_data
        dt, duration = task_data[3].split(' '), task_data[4]
        task_data[3], task_data[4] = dt[0], dt[1]
        task_data.append(duration)
        self.task_data = task_data
        await display_embed(self.task_data, self.task_id, title="Task created sucessfully!", del_after=86400, type='task')


