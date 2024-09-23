import urllib3
from bs4 import BeautifulSoup

def take_favicon(url):
    try:
        parsed_url = urllib3.util.parse_url(url)
    except Exception as err:
        print(err)
        return None

    http = urllib3.PoolManager()

    try:
        response = http.request('GET', url)
    except Exception as err:
        print(err)
        return None

    soup = BeautifulSoup(response.data)

    icon_link = None

    if soup.find("link", rel="shortcut icon"):
        icon_link = soup.find("link", rel="shortcut icon")
    else:
        icon_link = soup.find("link", rel="icon")
    print('21', icon_link)

    try:
        icon = icon_link['href']
        if parsed_url.scheme[0:4] == icon[0:4]:
            favicon = f'{icon}'
        else:
            favicon = f'{parsed_url.scheme}://{parsed_url.host}{icon}'

        print('21', favicon)
        if favicon:
         return favicon
        return None
    except Exception as err:
        print('31', err)
        return None


# import urllib3
# # from urllib.parse import urlparse
# from bs4 import BeautifulSoup
#
#
# def take_favicon(url):
#     try:
#         parsed_url = urllib3.util.parse_url(url)
#     except Exception as err:
#         print(err)
#         return None
#
#     print('7', parsed_url.scheme, parsed_url.host, parsed_url.path)
#     # print('6', url)
#     http = urllib3.PoolManager()
#     # print('8', http)
#     try:
#         # print('16')
#         response = http.request('GET', url)
#         # print('18', response)
#     except Exception as err:
#         print(err)
#         return None
#     # page = urllib3.urlopen(url)
#     soup = BeautifulSoup(response.data)
#     # print('13', soup)
#
#     icon_link = None
#     if soup.find("link", rel="shortcut icon"):
#         print('Shortcut Icon Found.')
#         icon_link = soup.find("link", rel="shortcut icon")
#     else:
#         icon_link = soup.find("link", rel="icon")
#         print('15', icon_link)
#
#     try:
#         icon = icon_link['href']
#         print('17', icon)
#
#         if parsed_url.scheme[0:4] == icon[0:4]:
#             print('Favicon Found.')
#             favicon = f'{icon}'
#         else:
#             print('Favicon Found.')
#             favicon = f'{parsed_url.scheme}://{parsed_url.host}{icon}'
#
#         print('21', favicon)
#         if favicon:
#             return favicon
#         return None
#     except Exception as err:
#         print('31', err)
#         return None
