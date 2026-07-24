"""
Giao diện chatbot Streamlit đơn giản cho K4 Lab.

Tái sử dụng các hàm/hằng số đã có trong template.py (không sửa template.py):
    - OPENAI_MODEL / OPENAI_MINI_MODEL  (đọc từ .env, tự động đúng luồng
      OpenAI/Gemini/NVIDIA mà bạn đang cấu hình)
    - count_tokens / estimate_cost      (Part 2)
    - retry_with_backoff                (Part 3)

Chạy:
    streamlit run streamlit_app.py
"""

import os

import streamlit as st
from openai import OpenAI

from template import (
    OPENAI_MINI_MODEL,
    OPENAI_MODEL,
    estimate_cost,
    retry_with_backoff,
)

MAX_TURNS = 5  # số lượt hội thoại (user+assistant) giữ lại trong lịch sử

st.set_page_config(page_title="LLM Chatbot", page_icon="💬")
st.title("💬 Chatbot LLM đơn giản")

# --- Sidebar: tham số điều chỉnh -------------------------------------------
with st.sidebar:
    st.header("Tham số")
    model = st.selectbox("Model", [OPENAI_MODEL, OPENAI_MINI_MODEL])
    persona = st.text_area(
        "System prompt (persona)",
        "Bạn là trợ lý AI hữu ích, trả lời ngắn gọn bằng tiếng Việt.",
    )
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Max tokens", 16, 1024, 256, 16)

    if st.button("🗑️ Xóa lịch sử"):
        st.session_state.messages = []
        st.rerun()

    st.caption(f"Lịch sử giữ tối đa {MAX_TURNS} lượt gần nhất.")

# --- Session state -----------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Hiển thị lịch sử chat ------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Nhận tin nhắn mới & gọi API ------------------------------------------
user_msg = st.chat_input("Nhập tin nhắn...")
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    api_messages = [{"role": "system", "content": persona}] + st.session_state.messages
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with st.chat_message("assistant"):
        placeholder = st.empty()
        reply = ""
        try:
            stream = retry_with_backoff(
                lambda: client.chat.completions.create(
                    model=model,
                    messages=api_messages,
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_tokens,
                    stream=True,
                )
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                reply += delta
                placeholder.markdown(reply + "▌")
            placeholder.markdown(reply)
        except Exception as e:
            reply = f"⚠️ Lỗi khi gọi API: {e}"
            placeholder.markdown(reply)


    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.messages = st.session_state.messages[-MAX_TURNS * 2 :]
