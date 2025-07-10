import requests
import re
import json
import os
from bs4 import BeautifulSoup


# Define the URL for the initial login request
login_url = 'https://cilteknik.com/'

# Define the headers
headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
  'cache-control': 'max-age=0',
  'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary8TgYDVJoDhKrs9x0',
  # Initial cookie - this will likely be updated after the first request
  'origin': 'https://cilteknik.com',
  'priority': 'u=0, i',
  'referer': 'https://cilteknik.com/',
  'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
}

# Define the data payload for the login form
KULLANICI_ADI = os.getenv("CILT_KULLANICI")
SIFRE = os.getenv("CILT_SIFRE")
if not KULLANICI_ADI or not SIFRE:
    raise ValueError("Gerekli environment değişkenleri tanımlı değil.")
  
login_data = '------WebKitFormBoundary8TgYDVJoDhKrs9x0\r\nContent-Disposition: form-data; name="KullaniciAdi"\r\n\r\n'+KULLANICI_ADI+'\r\n------WebKitFormBoundary8TgYDVJoDhKrs9x0\r\nContent-Disposition: form-data; name="Sifre"\r\n\r\n'+SIFRE+'\r\n------WebKitFormBoundary8TgYDVJoDhKrs9x0\r\nContent-Disposition: form-data; name="login-form-submit"\r\n\r\nlogin\r\n------WebKitFormBoundary8TgYDVJoDhKrs9x0--\r\n'



# Create a session to maintain cookies
session = requests.Session()

# Perform the login request
login_response = session.post(login_url, headers=headers, data=login_data)

# Check if login was successful (e.g., by checking the status code or redirect)
if login_response.status_code == 200:
    print("Login successful!")

    # Define the URL for the products page
    products_url = 'https://cilteknik.com/home/urunler/'

    # Go to the products page using the same session (which now has the updated cookies)
    products_response = session.get(products_url, headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': login_url, # Important to set the referer header
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
    })

    # Check if accessing the products page was successful
    if products_response.status_code == 200:
        print("Successfully accessed the products page.")
        html = products_response.text


        soup = BeautifulSoup(html, "lxml")

        urunler = []

        for tr in soup.find_all("tr"):
            try:
                img_tag = tr.find("img")
                img_url = img_tag.find_parent("a")["href"] if img_tag and img_tag.find_parent("a") else ""
                urun_kodu_td = tr.find_all("td")[2]
                urun_kodu = urun_kodu_td.get_text(strip=True)

                detay_link = tr.find("a", href=lambda x: x and x.startswith("/home/UrunDetay/"))
                urun_id = detay_link["href"].split("/")[-1]
                urun_adi = detay_link.get_text(strip=True)

                button = tr.find("button", attrs={"data-content": True})
                fiyat = ""
                fiyat_birimi = ""
                if button:
                    data_content = button["data-content"]
                    import re
                    match = re.search(r"Liste Fiyatı:\s*([\d,]+)\s*(EURO|USD|TL)", data_content)
                    if match:
                        fiyat = match.group(1)
                        curr = match.group(2)

                urunler.append({
                    "urun_kodu": urun_kodu,
                    "urun_adi": urun_adi,
                    "urun_id": urun_id,
                    "resim": img_url,
                    "fiyat": fiyat,
                    "fiyat_birimi": curr
                })


            except Exception as e:
                continue  # Bazı tr'ler boş olabilir, atla
        
        json.dump(urunler, open("urunler.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)
        print("file saved!")
    else:
        print(f"Failed to access the products page. Status code: {products_response.status_code}")
        print("Response content:")
        print(products_response.text) # Print the response to understand why it failed

else:
    print(f"Login failed. Status code: {login_response.status_code}")
    print("Response content:")
    print(login_response.text) # Print the response to understand why login failed
