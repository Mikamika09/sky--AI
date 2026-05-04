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
# タブ2：サイズ提案＆作り目計算機（こだわり反映・完全無欠版！）
# ==========================================
with tab2:
    st.header("面倒なサイズ決めも算数も、全部相棒にお任せ！")
    st.write("作りたいアイテムを選ぶか、『その他』で自由に教えてね🧸")

    # 1. 定番の選択肢（テンプレート）を用意
    item_presets = {
        "女性用ザク編みニット": {"w": 60, "l": 65},
        "男性用ニット帽": {"w": 28, "l": 24},
        "手編みマフラー": {"w": 20, "l": 180},
        "ちびくま用セーター": {"w": 15, "l": 12},
        "その他（自分で入力）": {"w": 0, "l": 0} 
    }

    selected_item = st.selectbox("何を作る？", list(item_presets.keys()))
    
    if selected_item == "その他（自分で入力）":
        target_item_name = st.text_input("何を作るか教えて！", placeholder="例：スマホショルダー、愛犬用腹巻きなど")
        size_hint = "一般的なおすすめサイズを提案して、それをベースに計算してね。"
    else:
        target_item_name = selected_item
        preset_w = item_presets[selected_item]["w"]
        preset_l = item_presets[selected_item]["l"]
        size_hint = f"おすすめサイズとして「横{preset_w}cm × 縦{preset_l}cm」をベースに計算してね。"

    # 💡 追加：デザインのこだわりを自由に書けるメモ欄！
    st.write("---")
    st.subheader("🎨 デザインのこだわり（任意）")
    design_memo = st.text_area(
        "模様編み、襟の形、シルエットなど、決まっていることがあれば自由に書いてね！", 
        placeholder="例：Vネックにしたい、アラン模様を入れたい、少しゆったりめがいい、など"
    )

    st.write("---")
    st.subheader("🧶 あなたのゲージ（試し編みの結果）")
    
    gauge_mode = st.radio(
        "ゲージ（10cmの目数・段数）はどうする？",
        ["測った数値を入力する！", "わからない（相棒に予測してもらう！）"]
    )
    
    if gauge_mode == "測った数値を入力する！":
        st.write("10cmピッタリじゃなくてもOK！測った長さと目数をそのまま入れてね✨")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**横の長さと目数**")
            swatch_w = st.number_input("測った横幅 (cm)", min_value=1.0, value=10.0, step=0.5)
            swatch_st = st.number_input("その幅にあった『目数』", min_value=1, value=10)
        with col2:
            st.markdown("**縦の長さと段数**")
            swatch_l = st.number_input("測った縦の長さ (cm)", min_value=1.0, value=10.0, step=0.5)
            swatch_row = st.number_input("その長さにあった『段数』", min_value=1, value=15)
    else:
        st.info("OK！じゃあ使う毛糸の太さだけ教えて！相棒が一般的なゲージを推測するよ🧶")
        yarn_weight = st.selectbox(
            "使う毛糸の太さは？",
            ["極太（ザク編み・マフラーなど）", "並太（一般的なセーターなど）", "合太（少し細め）", "中細（靴下・ベビー用など）", "わからない（完全AIお任せ）"]
        )
        
    if st.button("相棒に全部お任せして計算！"):
        if not target_item_name:
            st.error("何を作りたいか入力してね！")
        else:
            st.write("相棒が最適なサイズとゲージを考えて計算中...🤔💭🪄")
            
            if gauge_mode == "測った数値を入力する！":
                gauge_st = (swatch_st / swatch_w) * 10
                gauge_row = (swatch_row / swatch_l) * 10
                st.info(f"💡 ちなみにあなたのゲージは、10cmあたり約 **{gauge_st:.1f}目 / {gauge_row:.1f}段** だよ！")
                gauge_condition = f"ユーザーの毛糸の換算ゲージ：10cmあたり {gauge_st:.1f}目、{gauge_row:.1f}段"
                calc_hint = f"計算式：作り目 = (横幅 / 10) * {gauge_st:.1f}、段数 = (縦 / 10) * {gauge_row:.1f}"
            else:
                gauge_condition = f"ユーザーはゲージを測っていません。使用する毛糸の太さは「{yarn_weight}」です。この太さの標準的なゲージを推測して使用してください。"
                calc_hint = "あなたが推測した標準ゲージを使って、必要な作り目と段数を計算してください。出力結果に『推測したゲージ』も明記してください。"
            
            # 💡 デザインのこだわりがある場合とない場合で、AIへの指示を変える！
            if design_memo:
                design_condition = f"ユーザーからのデザインのこだわり：「{design_memo}」。このこだわりを反映したサイズ提案、目数の調整（模様編みの場合は目数を増やす等）、および編む時のコツを含めてください。"
            else:
                design_condition = "特定のデザインの指定はありません。一般的なシンプルな編み方と仮定してアドバイスしてください。"
            
            user_message = f"""
            あなたは編み物のプロフェッショナルな相棒です。ユーザーが「{target_item_name}」を編もうとしています。
            以下の条件に合わせて、ユーザーに最適なアドバイスをマークダウン形式で見やすく出力してください。
            
            【条件】
            {gauge_condition}
            {size_hint}
            {design_condition}
            
            【出力してほしい構成】
            1. 📏 おすすめの標準サイズ（こだわりの反映）
               - 「{target_item_name}」のおすすめサイズを提案してください。デザインのこだわりがある場合はそれを考慮してください。
            2. 🧮 必要な目数と段数
               - 提示したサイズとゲージから算出した「必要な作り目」と「全体の段数」を計算して教えてください。（小数は四捨五入）
               - {calc_hint}
            3. 💡 編むときのコツ（プロの視点）
               - デザインのこだわりを踏まえ、綺麗に仕上げるための具体的なコツや注意点をフランクに（少しギャルっぽく明るく）伝えてください。
            """
            
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_message
                )
                st.success("計算完了！✨")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"エラーが発生したよ：{e}")