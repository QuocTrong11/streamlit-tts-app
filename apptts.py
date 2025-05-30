import streamlit as st
import base64
import zlib
import requests

API_KEY = "YOUR_MINIMAX_API_KEY"  # <- Thay bằng khóa Minimax của bạn
TTS_URL = "https://api.minimax.chat/v1/tts"

def decode_deflate_base64(b64_string):
    try:
        compressed_data = base64.b64decode(b64_string)
        text = zlib.decompress(compressed_data, -zlib.MAX_WBITS).decode("utf-8")
        return text
    except Exception as e:
        return None

def call_minimax_tts(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice": "female_1",
        "format": "mp3"
    }

    response = requests.post(TTS_URL, headers=headers, json=data)

    if response.ok:
        return response.content
    else:
        return None

st.title("🔊 Trình phát giọng nói từ văn bản")

params = st.experimental_get_query_params()
b64_text = params.get("text", [None])[0]

if b64_text:
    st.markdown("**🔍 Đang giải mã...**")
    decoded_text = decode_deflate_base64(b64_text)

    if decoded_text:
        st.markdown(f"**📜 Văn bản gốc:** {decoded_text}")
        st.markdown("🎤 Đang tạo giọng nói...")
        audio = call_minimax_tts(decoded_text)
        if audio:
            st.audio(audio, format="audio/mp3")
        else:
            st.error("⚠️ Không thể gọi Minimax TTS.")
    else:
        st.error("❌ Không thể giải mã văn bản.")
else:
    st.warning("🔗 Không có tham số `text=` trong URL.")
