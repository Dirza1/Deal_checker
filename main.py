from playwright.sync_api import sync_playwright, Playwright
import time
from collections import defaultdict


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
    with open(file="html test", mode="w") as file:
        file.write(page.content())


if __name__ == "__main__":
    with sync_playwright() as playwright:
        main(playwright=playwright)
