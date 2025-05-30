import streamlit as st
import base64
import zlib
import requests
import time

API_KEY = ""
TTS_URL = "https://api.fpt.ai/hmi/tts/v5"

def decode_deflate_base64(b64_string):
    try:
        compressed_data = base64.b64decode(b64_string)
        # Dùng zlib thường (có header)
        text = zlib.decompress(compressed_data).decode("utf-8")
        return text
    except Exception as e:
        return None

def call_fpt_tts(text):
    headers = {
        'api-key': API_KEY,  # Sử dụng biến API_KEY đã định nghĩa
        'speed': '1',
        'voice': 'leminh'
    }
    response = requests.post(TTS_URL, data=text.encode('utf-8'), headers=headers)

    if response.status_code == 200:
        return response.json().get('async')  # Trích xuất URL âm thanh
    else:
        return None


st.title("🔊 Phát giọng nói từ văn bản (FPT.AI TTS)")

params = st.query_params
st.markdown(params)
b64_text = params.get("text", [None])
st.markdown(b64_text)
if b64_text:
    decoded_text = decode_deflate_base64(b64_text)
    if decoded_text:
        st.markdown(f"**📜 Văn bản:** {decoded_text}")
        st.markdown("🎤 Đang gọi FPT.AI TTS...")
        audio_url = call_fpt_tts(decoded_text)
        if audio_url and audio_url.startswith("http"):
            time.sleep(5)  # Đợi vài giây để API xử lý âm thanh
            st.audio(audio_url)
        else:
            st.error("Không thể tạo giọng nói. Kiểm tra lại dữ liệu.")
    else:
        st.error("❌ Không thể giải mã văn bản.")
else:
    st.warning("🔗 Không có tham số `text=` trong URL.")
