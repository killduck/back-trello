import urllib3
from bs4 import BeautifulSoup

def take_favicon(url):
    try:
        parsed_url = urllib3.util.parse_url(url)
    except Exception as ex:
        print(ex)
        return None

    http = urllib3.PoolManager()

    try:
        response = http.request('GET', url)
    except Exception as ex:
        print(ex)
        return None

    soup = BeautifulSoup(response.data, features="html.parser")

    icon_link = None

    if soup.find("link", rel="shortcut icon"):
        icon_link = soup.find("link", rel="shortcut icon")
    else:
        icon_link = soup.find("link", rel="icon")
    print('27', icon_link)

    try:
        icon = icon_link['href']
        if parsed_url.scheme[0:4] == icon[0:4]:
            favicon = f'{icon}'
        else:
            favicon = f'{parsed_url.scheme}://{parsed_url.host}{icon}'

        print('36', favicon)
        if favicon:
         return favicon
        return None
    except Exception as ex:
        print('41', ex)
        return None
