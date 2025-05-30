import streamlit as st
import base64
import zlib
import requests

API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiI0MS4gUXXhu5FjIFRy4buNbmciLCJVc2VyTmFtZSI6IjQxLiBRdeG7kWMgVHLhu41uZyIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTI4MTk4NTA4MjkzMTMyODA1IiwiUGhvbmUiOiIiLCJHcm91cElEIjoiMTkyODE5ODUwODI4ODkzODE2NyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6InRyYW50cm9uZzAxMDEyMDIxQGdtYWlsLmNvbSIsIkNyZWF0ZVRpbWUiOiIyMDI1LTA1LTMwIDEwOjMxOjAwIiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.s2ZQmCVFYwkyyJ9D3BxtMk3fVPZe9yRYVka1PW6uEDCMwSLJVoYikGPgUyiYMWTJScykuqT4OCyY1N78pHM5HKDM9WwO5bB7OHC08o7Nld4HaGTBRAdug3-dB3Ydv76J1GxPAXrFs5fT9xqV0aOSiEwpQROI1TrD7aGzCnqHSgL6yKQ3othfl9Zj9IDa0NWRExow7sGWbWD5rrvJcyn4fpyCXbvkuMg6ma4psrFoYOrGZNukurb22LtcH_eV5pwFhKq0jgqUEoW1b7skxkT0eBwZSGxxnCVjmGgKfjqMtCPB4ONXNDDada6wXu53Eo4_Wpy5p7jfvUThsw-EvmAMrA"  
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

params = st.query_params
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
