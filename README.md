# Music Recommendation System with Telegram Bot

![Python](https://img.shields.io/badge/Python-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange)

## Overview
This project is a music recommendation system integrated with a Telegram bot. It provides users with track recommendations based on Spotify data.

## How to Use
1. **Create Your Own Telegram Bot**
   - Go to Telegram's BotFather and create a new bot to get your bot token.
2. **Create a Spotify Developer Account**
   - Register at [Spotify Developer](https://developer.spotify.com/).
   - Create an app and obtain your `client_id` and `client_secret`.
3. **Set Up the Environment**
   - Install all necessary Python libraries.
4. **Prepare Files**
   - Create the following text files:
     - `token.txt` (contains your Telegram bot token)
     - `client_id.txt` (contains your Spotify `client_id`)
     - `client_secret.txt` (contains your Spotify `client_secret`)
   - Place these files in the root folder.
5. **Download the Dataset**
   - Download the `.csv` file from [Google Drive](https://drive.google.com/file/d/1S5utkUQuPEhpOHa7osUjKdCDXnynwHGP/view?usp=sharing).
   - Put the downloaded file inside the `data` folder.
6. **Run the Bot**
   - Execute the `tg_bot.py` script to start the Telegram bot.

## Future Work
- Add playlist recommendation functionality.
- Improve user interaction in the Telegram bot.
