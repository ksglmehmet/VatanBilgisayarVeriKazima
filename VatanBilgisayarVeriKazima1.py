# Vatan Bilgisayar Veri Kazıma
# Telefon Verilerini Çekmeye Çalışalım.

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# Bunlar ilk sayfası için. Tüm Sayfalar için Şu şekilde yapabiliriz. Sayfalar içinde gezinmemiz lazım.

ModelNos = []
Telefons = []
Fiyats = []
YorumSayisis = []
Scores = []
# Üstteki listeleri, for döngüsünde çıkan değerleri bunlara kaydedicem, bunlarıda sonra en son oluşturduğum dataframe'e yerleştirem.

for sayfa in range(1,16): # 15 sayfa var, 1-15 arasını alıyorum.
    
    print(f"{sayfa}. sayfanın veri kazımasına başlanıyor...")
    time.sleep(1)

    Url = f"https://www.vatanbilgisayar.com/cep-telefonu-modelleri/?page={sayfa}"

    # Response = requests.get(Url)
    # print(Response) Şu şekilde Daha kısa haliylede yazabiliriz.

    Parser = BeautifulSoup(requests.get(Url).content, "html.parser")

    # Find_all yerine find yazdım çünkü kendine özgü bir class'ı var(Telefonların genel tablosu). Telefonların ise aynı classları var. Ondan find_all kullandım.
    Veri = Parser.find("div", {"class": "wrapper-product wrapper-product--list-page clearfix"}).find_all("div", {"class": "product-list product-list--list-page"})
    # print(Veri)

    # Bunları liste haline çevirmiş oldum. Şimdi liste halinde olduğu için For döngüsüyle ihtiyacım olan veriyi alacağım. Her bilgiyi teker teker alacağım.

    for i in Veri:
        Telefon = i.find("div", {"class": "product-list__content"}).find("a", {"class": "product-list__link"}).find("div", {"class": "product-list__product-name"}).text.strip()
        Fiyat = i.find("div", {"class": "product-list__content"}).find("div", {"class": "product-list__cost"}).find("div", {"class": "productList-camp"}).find("span", {"class": "product-list__price"}).text.strip()
        ModelNo = i.find("div", {"class": "product-list__content"}).find("a", {"class": "product-list__link"}).find("div", {"class": "product-list__product-code"}).text.strip()
        YorumSayisi = i.find("div", {"class": "product-list__content"}).find("div", {"class": "wrapper-star"}).find("a", {"class": "comment-count"}).text.strip().replace("(","").replace(")","")
        Puani = i.find("div", {"class": "product-list__content"}).find("div", {"class": "wrapper-star"}).find("div", {"class": "rank-star"}).find("span", {"class": "score"})
        Score = Puani['style'].split(':')[1].strip().replace(';', '') if Puani and Puani.has_attr('style') else None
        ModelNos.append(ModelNo)
        Telefons.append(Telefon)
        Fiyats.append(Fiyat)
        YorumSayisis.append(YorumSayisi)
        Scores.append(Score)
        print(f"Telefon Adı: {Telefon.lstrip()}")
        print(f"Telefon Fiyatı: {Fiyat} TL'dir.")
        print(f"Model No: {ModelNo.lstrip()}") 
        print(f"Yorum Sayısı: {YorumSayisi.lstrip()}")
        print(f"Score: {Score.lstrip()}")
        print("\n")

    print(f"{sayfa}. sayfanın veri kazıması bitti...")
    time.sleep(1)

Urunler = pd.DataFrame({
    "Telefon Modeli": ModelNos,
    "Telefon İsmi": Telefons, 
    "Fiyat Bilgisi(TL)": Fiyats, 
    "Yorum Sayısı": YorumSayisis, 
    "Ürün Skoru": Scores})
# Urunler.head(20)

excel_adi = "C:/Users/Mehmet Akif/Desktop/vatan_telefon_verileri.xlsx"
Urunler.to_excel(excel_adi, index=False)

