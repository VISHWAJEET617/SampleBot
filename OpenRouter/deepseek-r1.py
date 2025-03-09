import telebot
import requests

# Replace '<YOUR_BOT_TOKEN>' with your bot's token
API_TOKEN = '<7299223546:AAEMkxNTEfBjmCwo7_CD8LRN43APIcxHeXw>'
bot = telebot.TeleBot(API_TOKEN)

# Welcome message for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = ("Welcome to the AI Chatbot! 🤖\n"
                    "Feel free to ask me anything. Just type your message and I'll respond.\n"
                    "To exit the chat, just type 'exit'.")
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(func=lambda message: True)
def respond_to_message(message):
    user_message = message.text
    chat_id = message.chat.id

    # Call OpenRouter API for chatbot response
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer <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>",  # Replace with your OpenRouter API key
        },
        json={
            "model": "deepseek/deepseek-r1:free",  # Specify the model to use
            "messages": [{"role": "user", "content": user_message}],  # User message
            "top_p": 1,
            "temperature": 0.9,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "repetition_penalty": 1,
            "top_k": 0,
        }
    )

    # Get the response from the OpenRouter API
    if response.status_code == 200:
        bot_response = response.json().get('choices', [{}])[0].get('message', {}).get('content', 'Sorry, I did not understand that.')
    else:
        bot_response = 'Error occurred while processing your request.'

    # Send the response back to the user
    bot.send_message(chat_id, bot_response)

# Start polling
bot.polling()
