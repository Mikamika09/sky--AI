from google import genai

# キラみかのAPIキー
GOOGLE_API_KEY = 'ここにAPIキーを入れる'
client = genai.Client(api_key=GOOGLE_API_KEY)

print("今使えるモデル一覧を検索中...")

# 使えるモデルの名前を全部出力する
for model in client.models.list():
    print(model.name)