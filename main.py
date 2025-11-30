from playwright.sync_api import sync_playwright, Playwright
import time
from collections import defaultdict
from bs4 import BeautifulSoup
import re

def main(playwright: Playwright):
    supermarket_url:defaultdict[str,str] = defaultdict(str,{
    "ah": "https://www.supermarktaanbiedingen.com/albert-heijn",
    "jumbo": "https://www.supermarktaanbiedingen.com/jumbo",
    "poiesz": "https://www.supermarktaanbiedingen.com/poiesz",
    "lidl": "https://www.supermarktaanbiedingen.com/lidl",
    "aldi": "https://www.supermarktaanbiedingen.com/aldi",
})

    chrome = playwright.chromium
    brouwser = chrome.launch(headless=True)
    page = brouwser.new_page()
    page.goto("https://www.supermarktaanbiedingen.com/aanbiedingen/albert_heijn",wait_until="networkidle")

    soup = BeautifulSoup(page.content(), "html.parser")
    aanbiedingen = soup.find_all(id=re.compile("product-"))
    print(len(aanbiedingen))
    with open("aanbiedingen",mode="w") as file:
        for aanbieding in aanbiedingen:
            Aanbieding_tietel = aanbieding.h3
            Aanbieding_text = aanbieding.p
            Oud_nieuw = aanbieding.find_all("span")
            if "beemster" in Aanbieding_tietel.text.lower():
                if len(Oud_nieuw) == 2:
                    file.write(f"Aanbieding: {Aanbieding_tietel.text}.\n Aanbieding text: {Aanbieding_text.text}.\n Oude Prijs: {Oud_nieuw[0].text}.\n Prijs nieuw: {Oud_nieuw[1].text if Oud_nieuw[1].text else None}.\n")
                    file.write("\n")
                else:
                    file.write(f"Aanbieding: {Aanbieding_tietel.text}.\n Aanbieding text: {Aanbieding_text.text}.\n")
                    file.write("\n")

if __name__ == "__main__":
    with sync_playwright() as playwright:
        main(playwright=playwright)
