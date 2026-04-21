# 💠 VisionAI Pro: Gelişmiş Görüntü Analiz Platformu

VisionAI Pro, **Groq LLaMA 4 Vision** teknolojisini kullanarak görselleri saniyeler içinde derinlemesine analiz eden, nesneleri tanımlayan ve teknik raporlar sunan profesyonel bir yapay zeka arayüzüdür.

![VisionAI Banner](https://img.shields.io/badge/AI-LLaMA--4-blue?style=for-the-badge&logo=ai)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)

---

## 🏗️ Proje Mimarisi

Aşağıdaki ağaç diyagramı, projenin modüler yapısını ve dosyaların işlevlerini göstermektedir:

```text
project_goruntu-all-130/
├── 📁 backend/             # Yerel kullanım için FastAPI motoru
│   └── app.py              # AI analiz endpointleri ve fallback mantığı
├── 📁 frontend/            # Yerel kullanım için Streamlit arayüzü
│   └── app.py              # Premium "Crystal Blue" UI bileşenleri
├── streamlit_app.py        # Streamlit Cloud için birleştirilmiş ana uygulama 🚀
├── start_app.py            # Backend ve Frontend'i tek tıkla başlatan script
├── requirements.txt         # Gerekli tüm Python kütüphaneleri
├── .env                    # API anahtarı ayarları (Yerel kullanım)
└── .gitignore              # Gizli dosyaların korunması
```

---

## 🌟 Öne Çıkan Özellikler

*   **LLaMA 4 Gücü**: En güncel görüntü işleme modelleri ile yüksek doğruluklu analiz.
*   **Crystal Blue Design**: Modern, glassmorphism içeren, kullanıcı dostu ve akışkan arayüz.
*   **Otomatik Dil Yönetimi**: %100 Türkçe analitik raporlama.
*   **Hızlı Dağıtım**: Hem yerel (Local) hem de bulut (Streamlit Cloud) ortamına tam uyumluluk.
*   **Akıllı Yedekleme (Fallback)**: Model kapasitesi dolduğunda otomatik olarak yedek AI modellerine geçiş.

---

## 🚀 Hızlı Başlangıç

### 1. Dosyaları Hazırlayın
Öncelikle repo'yu klonlayın ve bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

### 2. API Anahtarını Yapılandırın
`.env` dosyasını açın ve Groq API anahtarınızı ekleyin:
```env
GROQ_API_KEY=gsk_your_key_here
```

### 3. Uygulamayı Başlatın
Yerel ortamda hem backend'i hem frontend'i tek komutla çalıştırın:
```bash
python start_app.py
```

---

## ☁️ Streamlit Cloud Dağıtımı

Uygulamayı canlıya almak için GitHub hesabınızı Streamlit Cloud'a bağlayın ve `streamlit_app.py` dosyasını seçin. "Advanced Settings" kısmına API anahtarınızı `GROQ_API_KEY` adıyla eklemeyi unutmayın.

---

## 👤 Geliştirici
**Zeynep Ebrar PALA**  
*Yapay Zeka ve Görüntü İşleme Meraklısı*

---
© 2026 VisionAI Pro Ecosystem. Tüm hakları saklıdır.
