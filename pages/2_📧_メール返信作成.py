import streamlit as st

from utils.gemini_client import generate_text
from utils.history import add_history
from utils.ui import render_common_sidebar

st.set_page_config(page_title="メール返信作成", page_icon="📧")
model = render_common_sidebar()

st.title("📧 メール返信作成")
st.caption("受信したメールと返信の要点を入力すると、返信文の下書きを生成します。")

received_mail = st.text_area("受信したメールの本文", height=200, placeholder="相手から届いたメールを貼り付けてください")
key_points = st.text_area("返信で伝えたいこと(箇条書きでも可)", height=100, placeholder="例: 提案は承諾する、納期は来週金曜まで延ばしてほしい")
tone = st.selectbox("返信のトーン", ["丁寧・ビジネス", "フォーマル(取引先向け)", "カジュアル", "謝罪・お詫び"])

if st.button("返信文を生成", type="primary", disabled=not received_mail or not key_points):
    prompt = f"""あなたは優秀なビジネスアシスタントです。以下のメールへの返信文を作成してください。

# 受信したメール
{received_mail}

# 返信で伝えたい内容
{key_points}

# 返信のトーン
{tone}

宛名・署名を含む、そのまま送信できる形式のメール返信文を作成してください。"""
    with st.spinner("返信文を生成中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["email_result"] = result
            add_history("メール返信作成", key_points, result)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")

if "email_result" in st.session_state:
    st.markdown("### 生成結果")
    st.markdown(st.session_state["email_result"])
    st.text_area("コピー用テキスト", st.session_state["email_result"], height=250)
