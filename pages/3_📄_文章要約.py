import streamlit as st

from utils.gemini_client import generate_text
from utils.history import add_history
from utils.ui import render_common_sidebar

st.set_page_config(page_title="文章要約", page_icon="📄")
model = render_common_sidebar()

st.title("📄 文章要約")
st.caption("長い文章を貼り付けると、指定した形式で要約します。")

source_text = st.text_area("要約したい文章", height=300, placeholder="ここに長文を貼り付けてください")
summary_format = st.selectbox("要約の形式", ["一段落で要約", "箇条書きで要約", "一言(キャッチコピー風)で要約"])
summary_length = st.select_slider("要約の長さの目安", options=["短め", "普通", "やや詳しく"], value="普通")

if st.button("要約する", type="primary", disabled=not source_text):
    prompt = f"""以下の文章を要約してください。

# 要約する文章
{source_text}

# 要約の形式
{summary_format}

# 要約の長さ
{summary_length}

日本語で、元の文章の重要なポイントを漏らさず要約してください。"""
    with st.spinner("要約中..."):
        try:
            result = generate_text(prompt, model=model)
            st.session_state["summary_result"] = result
            add_history("文章要約", source_text[:50], result)
        except Exception as e:
            st.error(f"生成に失敗しました: {e}")

if "summary_result" in st.session_state:
    st.markdown("### 要約結果")
    st.markdown(st.session_state["summary_result"])
    st.text_area("コピー用テキスト", st.session_state["summary_result"], height=200)
