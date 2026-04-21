# streamlit_app.py
import streamlit as st
from groq import Groq
import base64
import os
from dotenv import load_dotenv
from PIL import Image
import io

# --- Sayfa Yapılandırması ---
st.set_page_config(
    page_title="VisionAI Pro | Akıllı Analiz Platformu",
    page_icon="💠",
    layout="wide",
)

# --- Ayar ve Gizlilik Yönetimi ---
load_dotenv()
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# --- Gelişmiş Premium CSS (Stabil Sürüm) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    :root {
        --primary-blue: #3b82f6;
        --secondary-blue: #60a5fa;
        --gold-accent: #FFD700;
        --bg-gradient: radial-gradient(circle at 50% 0%, #1e3a8a 0%, #020617 100%);
        --glass-bg: rgba(255, 255, 255, 0.04);
        --glass-border: rgba(255, 255, 255, 0.08);
    }

    [data-testid="stHeader"], [data-testid="stDecoration"] {
        display: none !important;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-gradient);
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Ana Konteynır - Küt Tasarım */
    [data-testid="stVerticalBlock"] > div:has(> [data-testid="stColumns"]) {
        background: var(--glass-bg);
        backdrop-filter: blur(30px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 3rem;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
        margin-top: 1rem;
    }

    /* Dosya Yükleyici - Tam Kontrol ve Koyu Tema (Simetrik) */
    [data-testid="stFileUploader"] {
        background-color: transparent !important;
    }
    
    [data-testid="stFileUploader"] section {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border: 2px dashed rgba(59, 130, 246, 0.5) !important;
        border-radius: 12px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 220px !important;
        padding: 2rem !important;
        position: relative !important;
    }

    /* Gözat Butonu */
    [data-testid="stFileUploader"] section button {
        background-color: var(--gold-accent) !important;
        color: #000 !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 2.5rem !important;
        margin-top: 110px !important; /* İkon ve metin için yer */
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
        z-index: 100;
    }

    /* 'Browse files' -> 'Gözat' */
    [data-testid="stFileUploader"] section button div div::before {
        content: "Gözat";
        visibility: visible;
    }
    [data-testid="stFileUploader"] section button div div {
        visibility: hidden;
    }
    
    [data-testid="stFileUploader"] section > div {
        display: none !important;
    }
    
    /* Profesyonel Bulut İkonu (Simetrik) */
    [data-testid="stFileUploader"] section::before {
        content: "";
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='50' height='50' viewBox='0 0 24 24' fill='none' stroke='%233b82f6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M17.5 19c2.5 0 4.5-2 4.5-4.5 0-2.3-1.7-4.2-3.9-4.5C17.4 6.7 14.5 4 11 4 8.2 4 5.8 5.7 4.7 8.1 2.6 8.8 1 10.7 1 13c0 2.8 2.2 5 5 5h1.5'/%3E%3Cpolyline points='11 13 14 10 17 13'/%3E%3Cline x1='14' y1='10' x2='14' y2='17'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: center;
        background-size: 50px;
        width: 100%;
        height: 50px;
        position: absolute;
        top: 40px;
        visibility: visible !important;
    }

    /* Açıklama Metni (Net Kontrast) */
    [data-testid="stFileUploader"] section::after {
        content: "Görseli buraya sürükleyin veya seçin";
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        position: absolute;
        top: 105px;
        width: 100%;
        text-align: center;
        visibility: visible !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* Analitik Rapor Kartı */
    .result-card-container {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 16px;
        padding: 2.5rem;
        border: 1px solid var(--glass-border);
        color: #e2e8f0;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.2);
    }

    .result-header {
        font-weight: 800; font-size: 1.8rem;
        background: linear-gradient(90deg, #FFD700, #ffffff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 1rem;
    }

    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        color: #cbd5e1;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        width: 100% !important;
    }

    .footer-text {
        text-align: center;
        color: #475569;
        font-size: 0.9rem;
        margin-top: 5rem;
        padding-bottom: 2rem;
    }
    .dev-name { color: var(--gold-accent); font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --- AI Analiz Fonksiyonu ---
def analyze_image(image_bytes, mime_type):
    if not api_key:
        return "Hata: API Anahtarı bulunamadı.", "N/A"
    
    client = Groq(api_key=api_key)
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    MODELS = ["meta-llama/llama-4-scout-17b-16e-instruct", "llama-3.2-11b-vision-preview"]
    
    for model_id in MODELS:
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "Sen dünyanın en iyi görüntü işleme ve analiz uzmanısın. Her türlü detayı fark edersin. Yanıtlarını çok yüksek doğrulukla ve sadece Türkçe olarak verirsin."},
                    {"role": "user", "content": [
                        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}},
                        {"type": "text", "text": """Bu resmi derinlemesine analiz et. Yanıtını şu formatta Türkçe ver:
1. **Ne var?** Detaylı özet.
2. **Kategori** Ana kategori.
3. **Alt Kategori** Özel sınıflandırma.
4. **Güven Skoru** % formatında.
5. **Detaylar** Renk, ışık, kompozisyon.
6. **Ek Bilgi** Teknik veya tarihsel bilgi."""}
                    ]}
                ],
                temperature=0.1,
            )
            return response.choices[0].message.content, model_id
        except:
            continue
    return "AI modelleri şu an meşgul, lütfen sonra tekrar deneyin.", "N/A"

# --- Arayüz Durumu ---
if 'analysed' not in st.session_state:
    st.session_state.analysed = False
if 'result_text' not in st.session_state:
    st.session_state.result_text = None
if 'image_bytes' not in st.session_state:
    st.session_state.image_bytes = None
if 'model_used' not in st.session_state:
    st.session_state.model_used = None

# --- Başlık Alanı (Restore Descriptive Text) ---
st.markdown("""
    <div style="text-align: center; padding-top: 2rem;">
        <h1 style="font-size: 4rem; font-weight: 800; color: #fff; margin-bottom: 0.5rem;">VisionAI Pro</h1>
        <p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; max-width: 800px; margin-inline: auto;">
            Bu uygulama, Groq LLaMA 4 Vision teknolojisini kullanarak yüklediğiniz her türlü görseli saniyeler içinde analiz eder, 
            nesneleri tanımlar ve teknik detaylar sunar.
        </p>
    </div>
""", unsafe_allow_html=True)

# Giriş Sayfası Detayları
if not st.session_state.analysed:
    _, mid_col, _ = st.columns([1, 2, 1])
    with mid_col:
        st.markdown("""
        <div class="info-box">
            <b>🚀 Neler Yapabilir?</b><br>
            • Nesne tanımlama ve profesyonel raporlama.<br>
            • Renk paleti, ışık ve kompozisyon analizi.<br>
            • Tamamen Türkçe rapor ve yüksek doğruluk.<br><br>
            <b>📏 Teknik Sınırlar:</b><br>
            • Formatlar: <b>JPG, PNG, WebP, BMP</b><br>
            • Maksimum Boyut: <b>200 MB</b><br>
            • Çözünürlük: Yüksek kalite daha iyi sonuç verir.
        </div>
        """, unsafe_allow_html=True)

# --- Ana Arayüz ---
with st.container():
    if not st.session_state.analysed:
        _, upload_col, _ = st.columns([1, 2, 1])
        with upload_col:
            uploaded_file = st.file_uploader("Görsel seçin", type=["jpg", "jpeg", "png", "webp", "bmp"], label_visibility="collapsed")
            if uploaded_file:
                st.session_state.image_bytes = uploaded_file.getvalue()
                st.image(st.session_state.image_bytes, use_container_width=True)
                if st.button("🔍 ANALİZİ BAŞLAT", use_container_width=True):
                    with st.spinner("AI Analizi yapılıyor..."):
                        res, model = analyze_image(st.session_state.image_bytes, uploaded_file.type)
                        st.session_state.result_text = res
                        st.session_state.model_used = model
                        st.session_state.analysed = True
                        st.rerun()
    else:
        left, right = st.columns([1, 1.2], gap="large")
        with left:
            st.markdown('<div class="section-header">🖼️ Analiz Edilen Görsel</div>', unsafe_allow_html=True)
            if st.session_state.image_bytes:
                st.markdown('<div style="border-radius:20px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);">', unsafe_allow_html=True)
                st.image(st.session_state.image_bytes, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            if st.button("◀️ Yeni Görsel Yükle"):
                st.session_state.analysed = False
                st.session_state.result_text = None
                st.rerun()
        with right:
            st.markdown(f"""
            <div class="result-card-container">
                <div class="result-header">📊 Analitik Rapor</div>
                <div style="font-size: 1.05rem; line-height: 1.6;">{st.session_state.result_text}</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"⚡ İşlem Motoru: {st.session_state.model_used}")

# --- Alt Bilgi ---
st.markdown(f"""
    <div class="footer-text">
        VisionAI Pro Ecosystem &copy; 2026 | Powered by Groq AI<br>
        Developed by <span class="dev-name">Zeynep Ebrar PALA</span>
    </div>
""", unsafe_allow_html=True)
