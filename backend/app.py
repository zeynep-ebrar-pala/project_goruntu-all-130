# backend/app.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import base64
import os
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

app = FastAPI(title="VisionAI Pro Görüntü Analiz Motoru")

# CORS Yapılandırması
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq İstemcisini Başlat
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY bulunamadı.")

client = Groq(api_key=api_key)

# Modeller
MODELS = [
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.2-11b-vision-preview"
]

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Görseli derinlemesine analiz eder. 
    Hata durumunda otomatik olarak yedek modellere geçer.
    """
    try:
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode('utf-8')
        content_type = file.content_type or "image/jpeg"
        
        last_error = None
        
        for model_id in MODELS:
            try:
                # Gelişmiş Sistem İstemi (Accuracy Improvement)
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {
                            "role": "system",
                            "content": "Sen dünyanın en iyi görüntü işleme ve analiz uzmanısın. Her türlü detayı (ışık, kompozisyon, nesne türleri, teknik özellikler) fark edersin. Yanıtlarını her zaman çok yüksek doğrulukla ve sadece Türkçe olarak verirsin."
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{content_type};base64,{base64_image}"
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": """Bu resmi en üst düzey dikkatle analiz et. Hiçbir detayı atlama. Yanıtını şu formatta Türkçe olarak ver:

1. **Ne var?** Görselin detaylı ve profesyonel özeti.
2. **Kategori** Ana kategori.
3. **Alt Kategori** Özel sınıflandırma.
4. **Güven Skoru** Analizine ne kadar güveniyorsun (% formatında).
5. **Detaylar** Renk paleti, ışık durumu, kompozisyon ve belirgin nesneler.
6. **Ek Bilgi** Görselle ilgili teknik veya tarihsel ilginç bir bilgi.

Yanıtın sadece Markdown formatında ve tamamen Türkçe olmalıdır. İngilizce terimlerden kaçın."""
                                }
                            ]
                        }
                    ],
                    max_tokens=1024,
                    temperature=0.1, # Daha tutarlı ve doğru sonuçlar için düşük sıcaklık
                )
                
                result = response.choices[0].message.content
                return {
                    "status": "success",
                    "model_used": model_id,
                    "result": result,
                    "filename": file.filename
                }
                
            except Exception as e:
                last_error = e
                continue 
        
        raise HTTPException(status_code=503, detail=f"AI modelleri şu an meşgul. Hata: {str(last_error)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {"status": "aktif", "message": "VisionAI Motoru Çalışıyor."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
