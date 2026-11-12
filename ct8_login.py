import os
import sys

import requests
from bs4 import BeautifulSoup

URL = "https://panel.ct8.pl/login/"
USER = os.environ["CT8_USER"]
PASSWORD = os.environ["CT8_PASS"]

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64)"

# 1. pobierz formularz (cookie + token CSRF + ukryte pola)
r = s.get(URL, timeout=30)
r.raise_for_status()
form = BeautifulSoup(r.text, "html.parser").find("form")
data = {i["name"]: i.get("value", "") for i in form.find_all("input") if i.get("name")}

# 2. login i hasło
data["username"] = USER
data["password"] = PASSWORD

# 3. wyślij formularz
r = s.post(URL, data=data, headers={"Referer": URL}, timeout=30)

# 4. sprawdź wynik
if r.ok and "/login" not in r.url:
    print("Zalogowano OK:", r.url)
else:
    print("Logowanie nie powiodło się:", r.status_code, r.url)
    soup = BeautifulSoup(r.text, "html.parser")
    for el in soup.select(".errorlist, .error, .alert, .message, [class*=error]"):
        print("Komunikat:", el.get_text(strip=True))
    print("Pola formularza:", list(data.keys()))
    sys.exit(1)
