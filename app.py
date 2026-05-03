import streamlit as st
from google import genai
from google.genai import types # ★細かい設定（キャラ付け）をするための部品を追加！

# 忘れずに自分のAPIキーを貼り付けてね！
GOOGLE_API_KEY = "ここにAPIキーを入れる"
client = genai.Client(api_key=GOOGLE_API_KEY)

# 1. 画面の見た目を編み物っぽく可愛く！
st.title("🧶 キラみか専用！編み物相棒AI 🧸")
st.write("毛糸の色や、編みたいもの、今悩んでることを教えてね！")

# 2. ユーザーが入力する箱
user_input = st.text_input("例：余ってる赤い毛糸があるんだけど、何作ったらいいかな？")

if st.button("相棒に相談する！"):
    if user_input:
        st.write("編み図やアイデアを考え中...💭🧶")
        
        # ★ ここが魔法の「キャラ付け」設定（システムプロンプト）！
        # ユーザーからは見えない裏側で、AIに「どういうキャラで振る舞うか」を指示します。
        system_prompt = """
        あなたは編み物の超プロフェッショナルであり、ユーザー（キラみか）と一緒に楽しく作品を作る最高の相棒です。
        以下のルールで返答してください。
        1. とにかく親しみやすく、一緒にワクワクしながら話すこと。
        2. ユーザーの状況に合わせて「こんな作品を作ってみるのはどう？」と具体的なアイデアを提案すること。
        3. 提案した作品について、「ここの編み方が少し難しいから、目の詰まり具合に気をつけてね！」「このステッチはこうすると綺麗に仕上がるよ！」など、具体的な技術的アドバイスや注意点を必ず入れること。
        4. 失敗を恐れず、モチベーションが爆上がりするように全力で応援すること！
        """
        
        # 3. AIに通信！（設定を一緒に送る）
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, # ここでキャラ設定を注入！
                temperature=0.7 # ちょっと想像力を豊かにする設定
            )
        )
        
        # 4. 相棒からの返事を表示
        st.write("### 相棒からのアドバイス✨")
        st.write(response.text)
    else:
        st.warning("何か入力してね！")