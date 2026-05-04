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
# タブ2：ゲージ・作り目計算機（超進化版！）
# ==========================================
with tab2:
    st.header("面倒な算数は相棒にお任せ！")
    st.write("作りたいアイテムを選ぶか、『その他』で自由に教えてね🧸")

    # 1. 定番の選択肢（テンプレート）を用意
    item_presets = {
        "女性用ザク編みニット": {"w": 60, "l": 65},
        "男性用ニット帽": {"w": 28, "l": 24},
        "手編みマフラー": {"w": 20, "l": 180},
        "ちびくま用セーター": {"w": 15, "l": 12},
        "その他（自分で入力）": {"w": 50, "l": 50}
    }

    # セレクトボックスを表示
    selected_item = st.selectbox("何を作る？", list(item_presets.keys()))
    
    # 「その他」が選ばれた時だけ、入力欄を出す魔法！
    if selected_item == "その他（自分で入力）":
        target_item_name = st.text_input("何を作るか教えて！", placeholder="例：スマホショルダー、愛犬用腹巻きなど")
    else:
        target_item_name = selected_item

    # 選択されたアイテムの標準値をセット
    default_w = item_presets[selected_item]["w"]
    default_l = item_presets[selected_item]["l"]

    st.write("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧶 あなたのゲージ")
        gauge_st = st.number_input("10cmあたりの『目数』", min_value=1, value=10)
        gauge_row = st.number_input("10cmあたりの『段数』", min_value=1, value=15)
        
    with col2:
        st.subheader("📏 作りたいサイズ(cm)")
        target_width = st.number_input("横幅", min_value=1, value=default_w)
        target_length = st.number_input("縦の長さ", min_value=1, value=default_l)
        
    if st.button("作り目と段数を計算！"):
        # 入力がない場合のガード
        if not target_item_name:
            st.error("何を作るか入力してね！")
        else:
            st.write("---")
            cast_on = int((target_width / 10) * gauge_st)
            total_rows = int((target_length / 10) * gauge_row)
            
            st.write(f"### 🧮 {target_item_name} の計算結果")
            st.info(f"✨ 必要な作り目： **{cast_on} 目**")
            st.info(f"✨ 必要な段数： **{total_rows} 段**")
            
            st.write(f"相棒（Gemini 2.5）が {target_item_name} のコツを伝授...🤔")
            
            # AIに「自由入力されたアイテム名」を渡してアドバイスをもらう！
            user_message = f"""
            今から「{target_item_name}」を編みます。
            サイズは 横{target_width}cm × 縦{target_length}cm。
            計算の結果、作り目{cast_on}目、総段数{total_rows}段になりました。
            このアイテム（{target_item_name}）を編む時のポイントや、綺麗に仕上げるコツを、編み物の先生としてフランクに教えて！
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message
            )
            st.success(response.text)