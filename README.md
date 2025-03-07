# Telegram Summarizer Bot

## Overview
A Telegram bot that generates concise summaries using OpenAI's API, allowing users to quickly extract key points from any text.

## Features
- Uses **OpenAI's GPT model** for text summarization
- Works in a conversational mode
- No need to restart for multiple summaries
- Simple and efficient Telegram bot integration

## Technologies Used
- **Python** for scripting and automation
- **OpenAI API** for natural language processing
- **python-telegram-bot** for bot interaction
- **dotenv** for managing environment variables

## How It Works
1. The user starts a conversation with `/start`.
2. Any text sent to the bot is processed and summarized.
3. The summarized output is sent back in a few bullet points.
4. The session can be ended with `/cancel`.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/polinamenshikova/Summify.git
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the script:
   ```sh
   python main.py
   ```

## License
This project is open-source under the MIT License.
