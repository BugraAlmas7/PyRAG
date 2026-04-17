import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    page.title = "Fortune App"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0e0018"
    page.padding = 0
    page.window_width = 390
    page.window_height = 844
    
    page.fonts = {
        "Mistik": "https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap",
    }
    page.theme = ft.Theme(font_family="Mistik")
    
    aktif_mod = {"tip": None} 
    aktif_label = {"kontrol": None} 

    ana_sahne = ft.Container(expand=True) 

    def dosya_secildi(e: ft.FilePickerResultEvent):
        if not e.files: return
        
        dosya_yolu = e.files[0].path
        mod = aktif_mod["tip"]
        label = aktif_label["kontrol"]
        
        if label:
            label.value = "Dosya alındı, analiz ediliyor... ⏳"
            label.update()

        try:
            with open(dosya_yolu, "rb") as f:
                data = {"file": f}
                
                if mod == "kahve":
                    res = requests.post(f"{API_URL}/analiz-kahve", files=data)
                    mesaj = res.json()["interpretation"]
                elif mod == "ruya":
                    res = requests.post(f"{API_URL}/analiz-ruya", files=data)
                    mesaj = res.json()["interpretation"]
                elif mod == "el":
                    res = requests.post(f"{API_URL}/analiz-el-fali", files=data)
                    mesaj = res.json()["interpretation"]
                elif mod == "tarot":
                    res = requests.post(f"{API_URL}/analiz-tarot-foto", files=data, params={"niyet": "Genel"})
                    mesaj = res.json()["interpretation"]
                elif mod == "ayna":
                    res = requests.post(f"{API_URL}/analiz-sihirli-ayna", files=data)
                    mesaj = f"Ayna: {res.json()['interpretation']}"
                else:
                    mesaj = "Bilinmeyen mod."

                if label:
                    label.value = mesaj
                    label.update()

        except Exception as hata:
            if label:
                label.value = f"Hata: {str(hata)}"
                label.update()

    secici = ft.FilePicker()
    secici.on_result = dosya_secildi
    page.overlay.append(secici)
    page.update()

    def sahne_degistir(icerik_listesi, baslik=None, geri_butonu=False):
        ust_bar = ft.Container()
        if baslik:
            sol_kisim = ft.Container(width=40)
            if geri_butonu:
                sol_kisim = ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color="#e0d0ff",
                    on_click=lambda _: ana_menuyu_getir()
                )
            
            ust_bar = ft.Container(
                padding=10, bgcolor="#1a002b",
                content=ft.Row(
                    [
                        sol_kisim,
                        ft.Text(baslik, size=20, weight="bold", color="#e0d0ff", font_family="Mistik"),
                        ft.Container(width=40)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )

        ana_sahne.content = ft.Column(
            [ust_bar] + icerik_listesi,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        ana_sahne.update()

    def menu_btn(isim, ikon_url, tiklama_func):
        return ft.Container(
            width=150, height=150, bgcolor="#240038", border_radius=20,
            border=ft.border.all(1, "#4b0082"),
            on_click=lambda _: tiklama_func(),
            content=ft.Column(
                [
                    ft.Image(src=ikon_url, width=60, height=60, color="#dcbfff"),
                    ft.Text(isim, size=16, weight="bold", color="white")
                ],
                alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def sayfa_kahve():
        sonuc = ft.Text("Fincanını yükle...", text_align="center")
        def tikla(e):
            aktif_mod["tip"] = "kahve"
            aktif_label["kontrol"] = sonuc
            secici.pick_files()
        
        sahne_degistir([
            ft.Container(height=20),
            ft.Image(src="https://cdn-icons-png.flaticon.com/512/3054/3054889.png", width=100, color="brown"),
            ft.Text("Neyse halim çıksın falim!", italic=True),
            ft.Container(height=20),
            ft.ElevatedButton("Fincan Yükle 📸", on_click=tikla, bgcolor="brown", color="white"),
            ft.Container(height=20),
            ft.Container(content=sonuc, padding=20, bgcolor="#240038", border_radius=10)
        ], baslik="Kahve Falı", geri_butonu=True)

    def sayfa_ruya():
        sonuc = ft.Text("Ses kaydını yükle...", text_align="center")
        def tikla(e):
            aktif_mod["tip"] = "ruya"
            aktif_label["kontrol"] = sonuc
            secici.pick_files()

        sahne_degistir([
            ft.Icon(name=ft.icons.BEDTIME, size=80, color="blue"),
            ft.ElevatedButton("Ses Dosyası Seç 🎙️", on_click=tikla, bgcolor="blue", color="white"),
            ft.Container(height=20),
            ft.Container(content=sonuc, padding=20, bgcolor="#240038", border_radius=10)
        ], baslik="Rüya Tabiri", geri_butonu=True)

    def sayfa_el():
        sonuc = ft.Text("El fotoğrafını yükle...", text_align="center")
        def tikla(e):
            aktif_mod["tip"] = "el"
            aktif_label["kontrol"] = sonuc
            secici.pick_files()

        sahne_degistir([
            ft.Icon(name=ft.icons.BACK_HAND, size=80, color="orange"),
            ft.ElevatedButton("El Fotoğrafı Seç ✋", on_click=tikla, bgcolor="orange", color="white"),
            ft.Container(height=20),
            ft.Container(content=sonuc, padding=20, bgcolor="#240038", border_radius=10)
        ], baslik="El Falı", geri_butonu=True)

    def sayfa_tarot():
        d_img = ft.Image(src="https://i.pinimg.com/736x/88/ed/5e/88ed5e8249822a10c710d0f5899d4546.jpg", width=200, height=350, border_radius=15)
        d_lbl = ft.Text("Karta dokun...", text_align="center")
        def d_tikla(e):
            d_lbl.value = "Kartlar çekiliyor..."
            d_lbl.update()
            try:
                res = requests.post(f"{API_URL}/analiz-tarot-dijital", json={"niyet": "Genel", "kart_sayisi": 1})
                d_img.src = "https://upload.wikimedia.org/wikipedia/commons/d/de/RWS_Tarot_01_Magician.jpg"
                d_lbl.value = res.json()['interpretation']
            except: d_lbl.value = "Hata oluştu."
            d_img.update()
            d_lbl.update()

        f_lbl = ft.Text("Fotoğraf yükle...", text_align="center")
        def f_tikla(e):
            aktif_mod["tip"] = "tarot"
            aktif_label["kontrol"] = f_lbl
            secici.pick_files()

        tabs = ft.Tabs(
            selected_index=0, 
            tabs=[
                ft.Tab(content=ft.Text("Dijital")), 
                ft.Tab(content=ft.Text("Foto Yükle"))
            ]
        )
        
        col_dijital = ft.Column([ft.Container(height=10), ft.Container(content=d_img, on_click=d_tikla), ft.Container(content=d_lbl, padding=10)], horizontal_alignment="center")
        col_foto = ft.Column([ft.Container(height=20), ft.ElevatedButton("Yükle", on_click=f_tikla), ft.Container(content=f_lbl, padding=10)], horizontal_alignment="center")

        govde = ft.Container(content=col_dijital)
        
        def tab_degis(e):
            govde.content = col_dijital if e.control.selected_index == 0 else col_foto
            govde.update()
        
        tabs.on_change = tab_degis
        sahne_degistir([tabs, govde], baslik="Tarot Falı", geri_butonu=True)

    def sayfa_burc():
        dd = ft.Dropdown(options=[ft.dropdown.Option(b) for b in ["Koç","Boğa","İkizler","Yengeç","Aslan","Başak","Terazi","Akrep","Yay","Oğlak","Kova","Balık"]], label="Burcun")
        lbl = ft.Text("Seç ve gör...", selectable=True)
        def getir(e):
            if not dd.value: return
            lbl.value = "Yıldızlara soruluyor..."
            lbl.update()
            try:
                res = requests.post(f"{API_URL}/analiz-burc", json={"burc": dd.value})
                lbl.value = res.json()["interpretation"]
            except: lbl.value = "Hata"
            lbl.update()
        
        sahne_degistir([dd, ft.ElevatedButton("Yorumla", on_click=getir), ft.Container(content=lbl, padding=20)], baslik="Günlük Burç", geri_butonu=True)

    def sayfa_ask():
        ad1 = ft.TextField(label="Senin Adın")
        ad2 = ft.TextField(label="Partnerin Adı")
        lbl = ft.Text("Bilgileri gir...", selectable=True)
        def hesapla(e):
            lbl.value = "Hesaplanıyor..."
            lbl.update()
            try:
                res = requests.post(f"{API_URL}/analiz-uyum", json={
                    "partner_1": {"isim": ad1.value, "dogum_tarihi": "01.01.1990", "dogum_saati": "12:00", "dogum_yeri": "x"},
                    "partner_2": {"isim": ad2.value, "dogum_tarihi": "01.01.1990", "dogum_saati": "12:00", "dogum_yeri": "x"}
                })
                lbl.value = res.json()["interpretation"]
            except: lbl.value = "Hata"
            lbl.update()

        sahne_degistir([ad1, ad2, ft.ElevatedButton("Analiz Et", on_click=hesapla), ft.Container(content=lbl, padding=20)], baslik="Aşk Uyumu", geri_butonu=True)

    def sayfa_ayna():
        chat_list = ft.ListView(expand=True, spacing=10, padding=20, height=400)
        msg_in = ft.TextField(hint_text="Yaz...", expand=True)
        
        def gonder(e):
            val = msg_in.value
            if not val: return
            chat_list.controls.append(ft.Text(f"Sen: {val}", color="grey"))
            msg_in.value = ""
            ana_sahne.update() 
            try:
                res = requests.post(f"{API_URL}/chat-sihirli-ayna", json={"history": [{"role":"user", "content":val}]})
                chat_list.controls.append(ft.Text(f"Ayna: {res.json()['content']}", color="white"))
                ana_sahne.update()
            except: pass

        def foto_bas(e):
            aktif_mod["tip"] = "ayna"
            temp = ft.Text("Fotoğraf analiz ediliyor...", color="yellow")
            chat_list.controls.append(temp)
            aktif_label["kontrol"] = temp
            secici.pick_files()
            ana_sahne.update()

        sahne_degistir([
            ft.Container(content=chat_list, bgcolor=ft.colors.with_opacity(0.2, "black"), border_radius=10),
            ft.Row([ft.IconButton(icon=ft.icons.CAMERA_ALT, on_click=foto_bas), msg_in, ft.IconButton(icon=ft.icons.SEND, on_click=gonder)])
        ], baslik="Sihirli Ayna", geri_butonu=True)

    def ana_menuyu_getir():
        satir1 = ft.Row([menu_btn("Rüya", "https://cdn-icons-png.flaticon.com/512/3656/3656986.png", sayfa_ruya), menu_btn("Kahve", "https://cdn-icons-png.flaticon.com/512/3054/3054889.png", sayfa_kahve)], alignment="center")
        satir2 = ft.Row([menu_btn("Tarot", "https://cdn-icons-png.flaticon.com/512/3309/3309995.png", sayfa_tarot), menu_btn("Ayna", "https://cdn-icons-png.flaticon.com/512/867/867906.png", sayfa_ayna)], alignment="center")
        satir3 = ft.Row([menu_btn("Aşk", "https://cdn-icons-png.flaticon.com/512/2530/2530869.png", sayfa_ask), menu_btn("Burç", "https://cdn-icons-png.flaticon.com/512/2647/2647306.png", sayfa_burc), menu_btn("El Falı", "https://cdn-icons-png.flaticon.com/512/5029/5029486.png", sayfa_el)], alignment="center")

        sahne_degistir([
            ft.Text("Kaderini Seç Fani...", size=16, color="grey"),
            ft.Divider(height=20, color="transparent"),
            satir1, ft.Divider(height=10, color="transparent"),
            satir2, ft.Divider(height=10, color="transparent"),
            satir3
        ], baslik="MİSTİK APP", geri_butonu=False)

    page.add(ana_sahne)
    ana_menuyu_getir()

ft.app(target=main)
