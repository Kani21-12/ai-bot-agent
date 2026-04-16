import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

reward = 0

print("🤖 AI Bot Started (type 'exit' to stop)\n")

while True:
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    # Generate AI response
    try:
        response = requests.post(
            url="https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "You are a helpful and friendly AI assistant."},
                    {"role": "user", "content": user_input}
                ]
            }
        )

        data = response.json()

        if "choices" in data:
            bot_reply = data["choices"][0]["message"]["content"]
        else:
            bot_reply = f"API Error: {data}"

    except Exception as e:
        bot_reply = f"Error: {e}"

    # Print bot response
    print("Bot:", bot_reply)

    # Reward system (as per assignment)
    if "good" in user_input.lower():
        reward += 1
    elif "bad" in user_input.lower():
        reward -= 1

    # Print reward score
    print("Reward Score:", reward)