# frontend/app.py
import streamlit as st
import requests
import os
from PIL import Image
import io
import time

# --- Sayfa Yapılandırması ---
st.set_page_config(
    page_title="VisionAI Pro | Akıllı Analiz Paneli",
    page_icon="💠",
    layout="wide",
)

# --- Gelişmiş Premium CSS ---
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

    /* Üst taraftaki beyaz çizgiyi (decoration) ve header'ı yok et */
    [data-testid="stHeader"], [data-testid="stDecoration"] {
        display: none !important;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-gradient);
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Ana Konteynır - Küt ve Bütünleşik Görünüm */
    [data-testid="stVerticalBlock"] > div:has(> [data-testid="stColumns"]) {
        background: var(--glass-bg);
        backdrop-filter: blur(30px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 3rem;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
        margin-top: 1rem;
    }

    /* Bölüm Başlıkları */
    .section-header {
        font-weight: 800;
        font-size: 1.8rem;
        background: linear-gradient(90deg, #93c5fd, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Dosya Yükleyici - Tam Kontrol ve Koyu Tema */
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
        min-height: 200px !important;
        padding: 2rem !important;
    }

    /* Browse Button - Gözat */
    [data-testid="stFileUploader"] section button {
        background-color: var(--gold-accent) !important;
        color: #000 !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        margin-top: 100px !important; /* İkon ve metin için yer aç */
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3) !important;
    }

    /* 'Browse files' metnini 'Dosya Seç' olarak değiştir */
    [data-testid="stFileUploader"] section button div div::before {
        content: "Gözat";
        visibility: visible;
    }
    [data-testid="stFileUploader"] section button div div {
        visibility: hidden;
    }
    
    [data-testid="stFileUploader"] section button:hover {
        background-color: #ffed4a !important;
        transform: scale(1.05) !important;
    }

    [data-testid="stFileUploader"] section > div {
        display: none !important; /* Orijinal metinleri tamamen gizle */
    }
    
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

    [data-testid="stFileUploader"] section::after {
        content: "Görseli buraya sürükleyin veya seçin";
        color: #ffffff !important; /* Tam beyaz kontrast */
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        position: absolute;
        top: 100px;
        width: 100%;
        text-align: center;
        visibility: visible !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }

    /* Analizi Başlat Butonu - Yüksek Kontrast */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
        text-transform: uppercase !important;
    }

    /* Analitik Rapor Kartı - Küt Tasarım */
    .result-card-container {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 16px;
        padding: 2.5rem;
        border: 1px solid var(--glass-border);
        color: #e2e8f0;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.2);
    }

    .result-header {
        font-weight: 800;
        font-size: 1.8rem;
        background: linear-gradient(90deg, #FFD700, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 1rem;
    }

    /* Görsel Çerçevesi ve Tarama Efekti */
    .img-frame {
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid var(--glass-border);
        position: relative;
    }
    .scan-line {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 4px;
        background: var(--primary-blue);
        box-shadow: 0 0 15px var(--primary-blue);
        animation: scanMove 3s ease-in-out infinite;
        z-index: 10;
    }
    @keyframes scanMove { 0% { top: 0%; } 100% { top:100%; } }

    /* Bilgilendirme Kutusu */
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        color: #cbd5e1;
    }

    /* Alt Bilgi */
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

# --- Uygulama Durumu ---
if 'analysed' not in st.session_state:
    st.session_state.analysed = False
if 'result_data' not in st.session_state:
    st.session_state.result_data = None
if 'image_bytes' not in st.session_state:
    st.session_state.image_bytes = None

# --- Başlık Alanı ---
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
            uploaded_file = st.file_uploader("Bir görsel yükleyin", type=["jpg", "jpeg", "png", "webp", "bmp"], label_visibility="collapsed")
            if uploaded_file:
                st.session_state.image_bytes = uploaded_file.getvalue()
                st.image(st.session_state.image_bytes, use_container_width=True)
                if st.button("🔍 ANALİZİ BAŞLAT", use_container_width=True):
                    with st.spinner("AI Analizi Gerçekleştiriliyor..."):
                        try:
                            files = {"file": (uploaded_file.name, st.session_state.image_bytes, uploaded_file.type)}
                            response = requests.post("http://localhost:8000/analyze", files=files, timeout=60)
                            if response.status_code == 200:
                                st.session_state.result_data = response.json()
                                st.session_state.analysed = True
                                st.rerun()
                            else:
                                st.error("Analiz sırasında hata oluştu.")
                        except Exception as e:
                            st.error(f"Bağlantı Hatası: {str(e)}")
    else:
        left_side, right_side = st.columns([1, 1.2], gap="large")
        
        with left_side:
            st.markdown('<div class="section-header">🖼️ Analiz Edilen Görsel</div>', unsafe_allow_html=True)
            if st.session_state.image_bytes:
                st.markdown('<div class="img-frame">', unsafe_allow_html=True)
                st.markdown('<div class="scan-line"></div>', unsafe_allow_html=True)
                st.image(st.session_state.image_bytes, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("◀️ Yeni Görsel Yükle", use_container_width=True):
                st.session_state.analysed = False
                st.session_state.result_data = None
                st.session_state.image_bytes = None
                st.rerun()

        with right_side:
            if st.session_state.result_data:
                st.markdown(f"""
                <div class="result-card-container">
                    <div class="result-header">📊 Analitik Rapor</div>
                    <div style="font-size: 1.05rem; line-height: 1.6;">{st.session_state.result_data["result"]}</div>
                </div>
                """, unsafe_allow_html=True)
                st.caption(f"⚡ İşlem Motoru: {st.session_state.result_data.get('model_used', 'VisionCore-Pro')}")

# --- Alt Bilgi ---
st.markdown(f"""
    <div class="footer-text">
        VisionAI Pro Ekosistemi &copy; 2026 | Groq AI Destekli<br>
        Geliştirici: <span class="dev-name">Zeynep Ebrar PALA</span>
    </div>
""", unsafe_allow_html=True)
