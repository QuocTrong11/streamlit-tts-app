import streamlit as st
import base64
import zlib
import requests
import time

API_KEY = "SBRGUwzOfB1UXqKUAgI6UF5FY2L6tw9A"
TTS_URL = "https://api.fpt.ai/hmi/tts/v5"

def decode_deflate_base64(b64_string):
    try:
        st.write(f"Chuỗi base64 nhận được: {b64_string}")  # In để kiểm tra
        compressed_data = base64.b64decode(b64_string)
        st.write(f"Dữ liệu đã giải mã base64: {compressed_data}")  # In để kiểm tra
        text = zlib.decompress(compressed_data, -zlib.MAX_WBITS).decode("utf-8")
        st.write(f"Văn bản đã giải nén: {text}")  # In để kiểm tra
        return text
    except Exception as e:
        st.error(f"Lỗi giải mã: {e}")
        return None

def call_fpt_tts(text, voice="banmai"):
    headers = {
        "api_key": API_KEY,
        "voice": voice,
        "speed": "0"
    }
    response = requests.post(TTS_URL, headers=headers, data=text.encode("utf-8"))
    if response.status_code == 200:
        data = response.json()
        st.write(f"Phản hồi từ FPT.AI: {data}")  # In toàn bộ phản hồi
        if data.get("error") == 0:  # Sử dụng .get() để tránh lỗi KeyError
            return data.get("async")  # Sử dụng .get() để tránh lỗi KeyError
    else:
        st.error(f"Lỗi khi gọi API FPT.AI: {response.status_code} - {response.text}")
    return None

st.title("🔊 Phát giọng nói từ văn bản (FPT.AI TTS)")

params = st.query_params
b64_text = params.get("text", [None])[0]

if b64_text:
    decoded_text = decode_deflate_base64(b64_text)
    if decoded_text:
        st.markdown(f"**📜 Văn bản:** {decoded_text}")
        st.markdown("🎤 Đang gọi FPT.AI TTS...")
        audio_url = call_fpt_tts(decoded_text)
        if audio_url:
            st.info(f"URL âm thanh nhận được: {audio_url}")  # In URL âm thanh
            time.sleep(5)  # Đợi vài giây để file sẵn sàng
            st.audio(audio_url)
        else:
            st.error("Không thể tạo giọng nói.")
    else:
        st.error("❌ Không thể giải mã văn bản.")
else:
    st.warning("🔗 Không có tham số `text=` trong URL.")
