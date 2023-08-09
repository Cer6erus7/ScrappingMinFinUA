import json
from pprint import pprint
import requests
import lxml
from bs4 import BeautifulSoup
from Errors import URLNotWorking


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
    return items

def parser():
    if get_html(URL).status_code == 200:
        print("OK")
    else:
        raise URLNotWorking("This URL doesn't work!")


if __name__ == "__main__":
    parser()