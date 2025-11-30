from playwright.sync_api import sync_playwright, Playwright
from collections import defaultdict
from bs4 import BeautifulSoup
import re
import datetime

def main(playwright: Playwright):
    supermarket_url:defaultdict[str,str] = defaultdict(str,{
    "ah": "https://www.supermarktaanbiedingen.com/aanbiedingen/albert_heijn",
    "jumbo": "https://www.supermarktaanbiedingen.com/aanbiedingen/jumbo",
    "poiesz": "https://www.supermarktaanbiedingen.com/aanbiedingen/poiesz",
    "lidl": "https://www.supermarktaanbiedingen.com/aanbiedingen/lidl",
    "aldi": "https://www.supermarktaanbiedingen.com/aanbiedingen/aldi",
})
    with open("te_vinden.log",mode="r",encoding="utf-8") as te_zoeken:
        acties = te_zoeken.read()
    
    zoek_lijst = acties.split(sep=",")
    print(len(zoek_lijst))

    chrome = playwright.chromium
    brouwser = chrome.launch(headless=True)
    with open("aanbiedingen",mode="w",encoding="utf-8") as file:
        for supermarked,url in supermarket_url.items():
            page = brouwser.new_page()
            file.write(f"AANBIEDIGEN VAN {supermarked.upper()}!\n")
            print(f"Supermarkt = {supermarked}, URL = {url}")
            page.goto(url=url,wait_until="networkidle")
            soup = BeautifulSoup(page.content(), "html.parser")
            aanbiedingen = soup.find_all(id=re.compile("product-"))
            print(len(aanbiedingen))
            
            for aanbieding in aanbiedingen:
                Aanbieding_tietel = aanbieding.h3
                Aanbieding_text = aanbieding.p
                if not Aanbieding_tietel or not Aanbieding_text:
                    continue
                Oud_nieuw = aanbieding.find_all("span")
                for actie in zoek_lijst:
                    if actie in Aanbieding_tietel.text.lower():
                        if len(Oud_nieuw) == 2:
                            file.write(f"Aanbieding: {Aanbieding_tietel.text}.\n"
                                    f"Aanbieding text: {Aanbieding_text.text}.\n"
                                    f"Oude Prijs: {Oud_nieuw[0].text}.\n "
                                    f"Prijs nieuw: {Oud_nieuw[1].text if Oud_nieuw[1].text else 'Onbekend'}.\n")                        
                            file.write("\n")
                        else:
                            file.write(f"Aanbieding: {Aanbieding_tietel.text}.\n"
                                    f"Aanbieding text: {Aanbieding_text.text}.\n")
                            file.write("\n")
                page.close()

    brouwser.close()

if __name__ == "__main__":
    #if datetime.date.today().weekday() == 0:
        with sync_playwright() as playwright:
            main(playwright=playwright) 
