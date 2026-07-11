import streamlit as st

from utils.gemini_client import AVAILABLE_MODELS, DEFAULT_MODEL, get_api_key


def render_common_sidebar() -> str:
    with st.sidebar:
        st.markdown("### ⚙️ 設定")
        if not get_api_key():
            st.error("GEMINI_API_KEY が未設定です。プロジェクト直下に .env を作成し設定してください。")
        model = st.selectbox(
            "使用モデル",
            AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(DEFAULT_MODEL),
            key="selected_model",
        )
    return model
