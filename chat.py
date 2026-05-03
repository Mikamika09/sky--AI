
import anthropic

client = anthropic.Anthropic(api_key="'ここにAPIキーを入れる'")

user_message = input("あなた: ")

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": user_message}
    ]
)

print("AI:", message.content[0].text)