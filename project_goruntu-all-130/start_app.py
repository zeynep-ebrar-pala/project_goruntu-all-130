# start_app.py
import subprocess
import time
import sys
import os

def start_services():
    print("🚀 AI Image Analysis System başlatılıyor...")
    
    # 1. Backend'i (FastAPI) arka planda başlat
    print("📦 Backend (FastAPI) başlatılıyor (Port 8000)...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Backend'in ayağa kalkması için kısa bir bekleme
    time.sleep(3)
    
    # 2. Frontend'i (Streamlit) başlat
    print("🎨 Frontend (Streamlit) başlatılıyor...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    print("\n✅ Sistem Hazır!")
    print("🔗 Frontend: http://localhost:8501")
    print("🔗 Backend API: http://localhost:8000")
    print("\nKapatmak için CTRL+C tuşlarına basın.")
    
    try:
        while True:
            time.sleep(1)
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("⚠️ Backend durdu!")
                break
            if frontend_process.poll() is not None:
                print("⚠️ Frontend durdu!")
                break
    except KeyboardInterrupt:
        print("\n🛑 Servisler kapatılıyor...")
        backend_process.terminate()
        frontend_process.terminate()
        print("👋 Görüşmek üzere!")

if __name__ == "__main__":
    start_services()
