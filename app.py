import streamlit as st
from google import genai
from google.genai import types

# ★ Streamlitの「秘密の金庫」から鍵を取り出す！
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=GOOGLE_API_KEY)

# --- 画面の基本設定 ---
st.set_page_config(page_title="編み物相棒AI", page_icon="🧶", layout="centered")
st.title("🧶 キラみか専用！編み物相棒AI 🧸")

# --- 🔓 簡易認証システム ---
# セッション状態を使って、一度パスワードが通れば再入力しなくていいようにするよ！
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🛡️ セキュリティ認証")
    password = st.text_input("合言葉を入れてね", type="password")
    if st.button("ログイン"):
        if password == "n&bku1biu793i": # ← 好きな合言葉に変えてもOK！
            st.session_state.authenticated = True
            st.rerun() # 画面をリフレッシュして中身を表示
        else:
            st.error("合言葉が違うよ！🤫")
    st.info("このアプリは関係者専用です。")
    st.stop() # ここで処理を止めて、下のコード（中身）を見せない

# --- 🏠 アプリの本編（認証が成功した時だけ実行される） ---
st.success("認証成功！相棒AIを起動したよ🧸✨")

# ★ Streamlitの魔法！画面を2つの「タブ」に分ける
tab1, tab2 = st.tabs(["🎨 完成イメージを作る", "🧮 ゲージ・作り目計算機"])


# ==========================================
# タブ1：完成イメージを作る（画像生成機能）
# ==========================================
with tab1:
    st.header("どんな作品を作りたい？")
    st.write("頭の中にあるイメージを教えて！AIが写真にして見せてくれるよ✨")
    
    image_prompt = st.text_input("例：春らしいパステルカラーの、透かし編みカーディガン")
    
    if st.button("完成イメージを見る！"):
        if image_prompt:
            st.write("毛糸を魔法で編んでるよ...🪄✨ 少々お待ちを！")
            
            try:
                # キラみかの見つけた最強モデルを指定！
                result = client.models.generate_images(
                    model='imagen-4.0-generate-001',
                    prompt=f"A high quality photo of a beautiful hand-knitted item: {image_prompt}",
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio="1:1"
                    )
                )
                
                generated_image_bytes = result.generated_images[0].image.image_bytes
                st.image(generated_image_bytes, caption="こんな感じの完成イメージはどう！？", use_container_width=True)
                st.success("モチベーション上がってきたね！さっそく編み始めよう！🔥")
                
            except Exception as e:
                st.error(f"エラー詳細：{e}")
        else:
            st.warning("どんなものを作りたいか入力してね！")


# ==========================================
# タブ2：ゲージ・作り目計算機
# ==========================================
with tab2:
    st.header("面倒な算数は相棒にお任せ！")
    st.write("ゲージ（10cm四方の目数・段数）と、作りたいサイズを入力してね。")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧶 あなたのゲージ")
        gauge_st = st.number_input("10cmあたりの『目数』", min_value=1, value=20)
        gauge_row = st.number_input("10cmあたりの『段数』", min_value=1, value=26)
        
    with col2:
        st.subheader("📏 作りたいサイズ")
        target_width = st.number_input("横幅 (cm)", min_value=1, value=50)
        target_length = st.number_input("縦の長さ (cm)", min_value=1, value=60)
        
    if st.button("作り目と段数を計算！"):
        st.write("---")
        
        cast_on = int((target_width / 10) * gauge_st)
        total_rows = int((target_length / 10) * gauge_row)
        
        st.write("### 🧮 計算結果")
        st.info(f"✨ 必要な作り目： **{cast_on} 目**")
        st.info(f"✨ 必要な段数： **{total_rows} 段**")
        
        st.write("相棒からのアドバイス...🤔")
        
        user_message = f"あなたは編み物の先生です。横{target_width}cm、縦{target_length}cm、作り目{cast_on}目、全部で{total_rows}段の作品を編むユーザーへ、2〜3行でフランクに励まして。"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message
        )
        st.success(response.text)