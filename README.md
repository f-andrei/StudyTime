# StudyTime Discord Bot

The StudyTime Discord Bot is an application developed for Discord with the aim of facilitating task management and providing alerts to assist in study routines.

## Features

1. **Task Management**
   - **/create_task:** Creates a new task.
   - **/tasks:** Lists all tasks. For each task there are buttons to Edit and Delete task.

2. **Note Management**
   - **/create_note:** Creates a new note.
   - **/notes:** Lists all notes. For each task there are buttons to Edit and Delete note.

3. **Chat with ChatGPT**
   - **/chat:** Initiates a conversation with ChatGPT to get answers to your questions or start a conversation.

4. **Alerts**
   - Alerts are automatically sent at scheduled times for each task.


## Installation Guide

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/f-andrei/StudyTime.git

2. **Install Requirements:** Navigate to the project directory and install the required Python packages using pip:
   
    ```bash
    cd StudyTime
    pip install -r requirements.txt
    ```

3. **Set Up OpenAI API Key:**
   - Visit [OpenAI's Quickstart Guide](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key) to obtain your API key.
   - Set up your API key as an environment variable. You can do this by adding the following line to your `.env` file in the project directory:
     
     ```plaintext
     OPENAI_API_KEY=your_api_key_here
     ```

4. **Set Up Environment Variables:**
   - Create a `.env` file in the project directory if it doesn't already exist.
   - Define the necessary environment variables in the `.env` file. For example:
     
     ```plaintext
     DISCORD_TOKEN=your_discord_bot_token_here
     CHANNEL_ID=your_discord_channel_id_here
     DISCORD_ID=your_discord_user_id_here
     ```
   - Refer to the [Discord Developer Portal](https://discord.com/developers/docs/getting-started#configuring-your-bot) to learn how to obtain your Discord bot token.
   - Learn how to find your Discord server's ID and channel ID in [this article](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID).

5. **Run the Bot:** Start the bot by running the main Python script:
   
    ```bash
    python main.py
    ```

6. **Invite the Bot to Your Discord Server:**
   - Visit the Discord Developer Portal and create a new application.
   - Add a bot to your application and copy the bot token.
   - Use the bot token to invite the bot to your Discord server using the following link (replace `<YOUR_BOT_CLIENT_ID>` with your bot's client ID):
     
     ```plaintext
     https://discord.com/oauth2/authorize?client_id=<YOUR_BOT_CLIENT_ID>&scope=bot
     ```

7. **Enjoy Using the StudyTime Discord Bot!** You can now use the bot's commands and features on your Discord server.

