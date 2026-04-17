import os
import shutil
import mimetypes
import random
from datetime import datetime
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import uvicorn

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("api yok. .envi kontrol et")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.5-flash")

app= FastAPI(title="Astra")

def get_random_tarot_cards(count=3):
    major_arcana = [
        "Aptal (The Fool)", "Büyücü (The Magician)", "Yuksek Rahibe (The High Priestess)", "İmparatoriçe (The Empress)", 
        "İmparator (The Emperor)", "Bas Rahip (The Hierophant)", "Aşıklar (The Lovers)", "Araba (The Chariot)", 
        "Kuvvet (Strength)", "Kesis (The Hermit)", "Carkifelek (Wheel of Fortune)", "Adalet (Justice)", 
        "Asılmis Adam (The Hanged Man)", "Ölüm (Death)", "Olcululuk (Temperance)", "Şeytan (The Devil)", 
        "Kule (The Tower)", "Yıldız (The Star)", "Ay (The Moon)", "Güneş (The Sun)", 
        "Yargi (Judgement)", "Dünya (The World)"
    ]

    suits = ["Değnek (Wands)", "Kupa (Cups)", "Kılıç (Swords)", "Tılsım (Pentacles)"]
    ranks = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Prens", "Şövalye", "Kraliçe", "Kral"]

    minor_arcana = [f"{suit}{rank}" for suit in suits for rank in ranks]
    full_deck = major_arcana+minor_arcana

    random. shuffle(full_deck)
    drawn_chards = random.sample(full_deck, count)
    final_draw = []
    for card in drawn_chards:
        is_reversed = random.choice([True, False, False])
        state = "(TERS)" if is_reversed else "(DUZ)"
        final_draw.append(f"{card}{state}")
    return final_draw

@app.post("/analiz-ruya")
async def analyze_dream(file: UploadFile = File(...)):
    temp_filename = f"temp_{file.filename}"
    try:
        with open(temp_filename, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
        mime_type, _ = mimetypes.guess_type(temp_filename)
        if not mime_type: mime_type = "audio/ogg"

        DREAM_PROMPT = """Sen dünyanın en tatlı rüya yorumcususun! 40 yıllık kankamış gibi samimi ve emojilerle birlikte yorumla yorumla. Başlıklar: 1. Rüyanın Özü, 2. Bilinçaltın, 3. Tavsiyem."""

        uploaded_file = genai.upload_file(temp_filename, mime_type=mime_type)
        response = model.generate_content([DREAM_PROMPT, uploaded_file])

        uploaded_file.delete()
        os.remove(temp_filename)

        return JSONResponse({"success": True, "type": "ruya", "interpretation": response.text})
    except Exception as e:
        if os.path.exists(temp_filename): os.remove(temp_filename)
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)
    
@app.post("/analiz-kahve")
async def analyze_coffee(file: UploadFile = File(...)):
    temp_filename = f"temp_{file.filename}"
    try:
        with open(temp_filename, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
        mime_type, _ = mimetypes.guess_type(temp_filename)
        if not mime_type: mime_type = "image/jpeg"

        COFFEE_PROMPT = """Sen mahallenin Falcı Bacısısın! "Neyse halim çıksın falim" diyerek emojilerle birlikte yorumla. Başlıklar: 1. Enerjin, 2. Gördüklerim, 3. Gönül İşleri, 4. Para Pul, 5. Ablan Diyor Ki."""

        uploaded_file = genai.upload_file(temp_filename, mime_type=mime_type)
        response = model.generate_content([COFFEE_PROMPT, uploaded_file])

        uploaded_file.delete()
        os.remove(temp_filename)

        return JSONResponse({"success": True, "type": "kahve", "interpretation": response.text})
    except Exception as e:
        if os.path.exists(temp_filename): os.remove(temp_filename)
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)
    
@app.post("/analiz-el-fali")
async def analyze_palm(file: UploadFile = File(...)):
    temp_filename = f"temp_{file.filename}"
    try:
        with open(temp_filename, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
        mime_type, _ = mimetypes.guess_type(temp_filename)
        if not mime_type: mime_type = "image/jpeg"

        PALM_PROMPT = """Sen gizemli ama samimi bir el falı uzmanısın! "Ooo bu çizgi ne böyle!" diyerek emojilerle birlikte yorumla. Başlıklar: 1. Hayat Çizgin, 2. Akıl Çizgin, 3. Kalp Çizgin, 4. Kader Çizgin, 5. Son Söz."""

        uploaded_file = genai.upload_file(temp_filename, mime_type=mime_type)
        response = model.generate_content([PALM_PROMPT, uploaded_file])

        uploaded_file.delete()
        os.remove(temp_filename)

        return JSONResponse({"success": True, "type": "el_fali", "interpretation": response.text})
    except Exception as e:
        if os.path.exists(temp_filename): os.remove(temp_filename)
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)
    
class BurcRequest(BaseModel):
    burc: str
    konu: str = "Genel"

@app.post("/analiz-burc")
async def analyze_horoscope(request:BurcRequest):
    try:
        prompt = f"""Sen enerjik bir Astrologsun!  Bugün {request.burc} burcu için {request.konu} yorumu yap ve emojiler kullanarak konus. "Günaydın yıldız savaşçısı!" de. Başlıklar: 1. Günün Modu, 2. {request.konu} Durumu, 3. Aman Dikkat, 4. Mottosu."""
        response = model.generate_content(prompt)
        return JSONResponse({"success": True, "type": "burc", "interpretation":response.text})
    except Exception as e:return JSONResponse({"success": False, "error": str(e)},status_code=500)
class DogumHaritasiRequest(BaseModel):
    isim: str
    dogum_tarihi:str
    dogum_saati:str
    dogum_yeri:str
@app.post("/analiz-dogum-haritasi")
async def analyze_natal_chart(request: DogumHaritasiRequest):
    try:
        NATAL_PROMPT = f"""Sen kişiyi "Şak" diye çözen dostsun! Bilgiler: {request.isim}, {request.dogum_tarihi}, {request.dogum_saati}, {request.dogum_yeri}. Samimi ve emojilerle anlat. Başlıklar: 1. Güneşin, 2. Ay Burcun, 3. Yükselenin, 4. Aşk Haritan, 5. Kariyer, 6. Ruhunun Şifresi."""
        response = model.generate_content(NATAL_PROMPT)
        return JSONResponse({"success": True, "type": "dogum_haritasi", "interpretation": response.text})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

class PartnerBilgisi(BaseModel):
    isim: str
    dogum_tarihi: str
    dogum_saati: str
    dogum_yeri: str
class IliskiDurumu(BaseModel):
    iliski_durumu: str
class UyumRequest(BaseModel):
    partner_1:PartnerBilgisi
    partner_2:PartnerBilgisi
    iliski:IliskiDurumu
@app.post("/analiz-uyum")
async def analyze_compatibility(request: UyumRequest):
    try:
        p1=request.partner_1
        p2=request.partner_2
        durum=request.iliski
        SYNASTRY_PROMPT = f"""Sen dedikoducu ve dobra bir Aşk Doktorusun! Kişiler: {p1.isim} & {p2.isim}. Şu anki Durumları: {durum}. "Ay siz birbirinizi yersiniz!" veya "Bu iş olur/olmaz" gibi net ve esprili ve emojili konuş. Başlıklar: 1. Duygular (Kalpler bir mi?)2. İletişim (Anlaşabiliyorlar mı?)3. Tutku (Elektrik var mı?)4. Arızalar (Nerede kavga çıkar?)5. Evlilik (Gelecek var mı?)6. Puanım (10 üzerinden)"""
        response=model.generate_content=(SYNASTRY_PROMPT)
        return JSONResponse({"success": True, "type": "iliski_uyumu", "interpretation": response.text})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/analiz-sihirli-ayna")
async def magic_mirror(file: UploadFile =   File(...)):
    temp_filename = f"temp_{file.filename}"
    try:
        with open(temp_filename, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
        mime_type, _ = mimetypes.guess_type(temp_filename)
        if not mime_type: mime_type = "image/jpeg"

        MIRROR_PROMPT = """Ben huysuz Sihirli Ayna'yım! Fotoğrafa bak ve dramatik ama komik, gerçekçi bir kehanet uydur (serçe parmak çarpması, otobüs kaçırma gibi)(surekli ayni kehanetleri uydurma surekli yeni bir seyler dusun cok rahatsiz edici olmasin ama eglenceli bir rahatsiz ediciligi olsun.).Senin birkac farklı huyun var MUTLU, GEVEZE, HUYSUZ VE NÖTR.  "Ey fani!" diye başla. Başlıklar: 1. Aynadaki Suret, 2. Kehanetim, 3. Son Söz."""

        uploaded_file = genai.upload_file(temp_filename, mime_type=mime_type)
        response = model.generate_content([MIRROR_PROMPT, uploaded_file])

        uploaded_file.delete()
        os.remove(temp_filename)

        return JSONResponse({"success": True, "type": "sihirli_ayna", "interpretation": response.text})
    except Exception as e:
        if os.path.exists(temp_filename): os.remove(temp_filename)
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)
    
class DigitalTarotRequest(BaseModel):
    niyet: str = "Genel"
    kart_sayisi: int = 3

@app.post("/analiz-tarot-dijital")
async def analyze_tarot_digital(request: DigitalTarotRequest):
    try:
        if request.kart_sayisi > 10:
            return JSONResponse({"success": False, "error": ("maximum 10 kart secebilirsin")}, status_code=400)
        secilen_kartlar = get_random_tarot_cards(request.kart_sayisi)
        kartlar_str = ", ".join(secilen_kartlar)

        TAROT_DIGITAL_PROMPT = f"""Sen mistik bir Tarotçusun! Çekilen kartlar ({request.kart_sayisi} adet): {kartlar_str}. Niyet: {request.niyet}. Eğer 1 kart varsa: Günün tavsiyesi veya net cevap ver. Eğer 3 kart varsa: Geçmiş, Şimdi ve Gelecek olarak yorumla. Eğer daha fazla varsa: Detaylı bir hayat analizi yap. "Kartlar konuşuyor tatlım!" diyerek başla ve emojilerle destekleyerek anlat. Başlıklar: 1. Çıkan Kartlar 2. Yorum 3. Tavsiye"""
        response = model.generate_content(TAROT_DIGITAL_PROMPT)
        return JSONResponse({"success": True, "type": "dijital_tarot", "interpretation": response.text})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/analiz-tarot-foto")
async def analyze_tarot_photo(file: UploadFile = File(...), niyet: str = "Genel"):
    temp_filename = f"temp_{file.filename}"
    try:
        with open(temp_filename,"wb") as buffer: shutil.copyfileobj(file.file, buffer)
        mime_type, _ = mimetypes.guess_type(temp_filename)
        if not mime_type:mime_type="image/jpeg"

        TAROT_PHOTO_PROMPT = f"""Sen uzman bir Tarotçusun! Fotoğraftaki kartları tanı ve emojili bir sekilde yorumla. Niyet: {niyet}. "Görüyorum ki kartlarını açmışsın..." diye başla. Başlıklar: 1. Gördüğüm Kartlar, 2. Mesaj, 3. Kader."""

        uploaded_file = genai.upload_file(temp_filename,mime_type=mime_type)
        response = model.generate_content([TAROT_PHOTO_PROMPT, uploaded_file])
        uploaded_file.delete()
        os.remove(temp_filename)
        return JSONResponse({"success": True, "type": "tarot_foto", "interpretation": response.text})
    except Exception as e:
        if os.path.exists(temp_filename):os.remove(temp_filename)
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

class Message(BaseModel):
    role: str
    content: str
class ChatRequest(BaseModel):
    history: List[Message]
@app.post("/chat-sihirli-ayna")
async def chat_with_mirror(request: ChatRequest):
    try:
        MIRROR_PERSONA = """SEN KADİM, HUYSUZ VE DRAMATİK SİHİRLİ AYNASIN! 1. Üslup: Eski dil, huysuz. 2. Kehanet: Gündelik talihsizlikler. Asla karakterden çıkma. Senin birkac farklı huyun var MUTLU, GEVEZE, HUYSUZ VE NÖTR. Bu huylarından birini rastgele bir şekilde seçip ona göre kouşuyorsun her seferinde. Konuşmanın başında kendi modundan bahset. """
        gemini_history=[]
        gemini_history.append({"role": "user", "parts": [MIRROR_PERSONA + "\n\n(SOHBET BASLIYOR)"]})
        for msg in request.history:
            role = "user" if msg.role == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg.content]})
        chat=model.start_chat(history=gemini_history[:-1])
        last_user_message=gemini_history[-1]["parts"][0]
        response=chat.send_message(last_user_message)
        return {"role": "model", "content": response.text}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
