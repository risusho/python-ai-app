import streamlit as st

from utils.gemini_client import AVAILABLE_MODELS, DEFAULT_MODEL, get_api_key


def render_common_sidebar() -> str:
    with st.sidebar:
        st.markdown("### ⚙️ 設定")
        st.text_input(
            "Gemini APIキー",
            type="password",
            key="user_api_key",
            help="Google AI Studio (https://aistudio.google.com/apikey) で発行したAPIキーを入力してください。"
            "入力したキーはこのブラウザセッション内でのみ使用され、サーバーには保存されません。",
        )
        if not get_api_key():
            st.error("Gemini APIキーが未設定です。上の欄にAPIキーを入力してください。")
        model = st.selectbox(
            "使用モデル",
            AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(DEFAULT_MODEL),
            key="selected_model",
        )
    return model
