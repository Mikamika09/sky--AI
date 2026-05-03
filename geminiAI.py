from google import genai

# ★ 今使っている、日本語が入っていない純度100%のAPIキーを貼り付け！
GOOGLE_API_KEY = 'ここにAPIキーを入れる'

client = genai.Client(api_key=GOOGLE_API_KEY)

print("AIに通信中...")

prompt = "こんにちは！私はキラみかです。一言挨拶して！"

# ★ リストで見つけた最新モデル「gemini-2.5-flash」を指定！
response = client.models.generate_content(
    model='gemini-flash-latest',
    contents=prompt
)

print("AIの返答：")
print(response.text)