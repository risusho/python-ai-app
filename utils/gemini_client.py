from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

DEFAULT_MODEL = "gemini-2.5-flash"
AVAILABLE_MODELS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-3.5-flash"]


def get_api_key() -> str | None:
    user_key = st.session_state.get("user_api_key")
    if user_key:
        return user_key
    return os.environ.get("GEMINI_API_KEY")


@st.cache_resource
def _get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


def generate_text(prompt: str, model: str = DEFAULT_MODEL, temperature: float = 0.7) -> str:
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("APIキーが設定されていません。サイドバーにGemini APIキーを入力してください。")

    client = _get_client(api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperature),
    )
    return response.text
