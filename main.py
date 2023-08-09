import json
from pprint import pprint
import requests
import lxml
from bs4 import BeautifulSoup
from Errors import URLNotWorking, NotEnoughCards


HOST = "https://minfin.com.ua/"
URL = "https://minfin.com.ua/cards/"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
}


def get_html(url, params=""):
    return requests.get(url, headers=HEADERS, params=params)

def get_content(html):
    soup = BeautifulSoup(html.text, "lxml")
    cards = soup.find_all("div", class_='be80pr-2 gFPIhv')
    items = []

    for item in cards:
        items.append(
            {'title': item.find('div', class_='be80pr-15 kwXsZB').find('a', class_="cpshbz-0 eRamNS").text,
             'link_product': HOST + item.find('a', class_='cpshbz-0 eRamNS').get("href"),
             'brand': item.find('div', class_='be80pr-16 be80pr-17 kpDSWu cxzlon').find("a").get("alt"),
             'img_url': item.find('div', class_="be80pr-9 fJFiLL").find("img").get("srcset").split()[2]}
        )

    with open('db.json', 'w') as f:
        json.dump(items, f, indent=2)

def parser():
    amount = int(input("Write amount of cards - "))
    count = 0
    with open("db.json", 'r') as f:
        cards = json.load(f)
        if len(cards) < amount:
            raise NotEnoughCards("There are not many cards!")
        for card in cards:
            if count == amount: break
            print("Card's name: " + card['title'] + "\nBrand's name: " + card["brand"] +
                  "\nImage_url: " + card["img_url"] + "\nProduct's link: " + card["link_product"] + "\n")
            count += 1


if __name__ == "__main__":
    get_content(get_html(URL))
    parser()