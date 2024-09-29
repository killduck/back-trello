from ..models import Card, CardFile, CardLink, ImageExtension
from ..serializers import ImageExtensionSerializer

import urllib3
from bs4 import BeautifulSoup

class AddFileAndLink:
    request = None
    image_bool = False
    img_extensions = ImageExtensionSerializer(ImageExtension.objects.all(), many=True).data

    link_id = None
    request_link_first_letter = None

    icon_link = None
    request_link = None

    error_file = None
    error_link = None

    def __init__(self, request):
        self.request = request
        self.add_file()
        self.add_link()

    def add_file(self):
        try:
            file_list = self.request.getlist('file')
            for file in file_list:
                print('78__>>>', file.name.split('.')[-1])
                request_file_extension = file.name.split('.')[-1]

                for img_extension in self.img_extensions:
                    if request_file_extension == img_extension['type']:
                        print(f'89__ {request_file_extension, img_extension['type']}')
                        self.image_bool = True

                CardFile.objects.create(
                    card=Card.objects.get(id=self.request['card_id']),
                    name=file.name,
                    size=file.size,
                    extension=request_file_extension,
                    file_url=file,
                    image=self.image_bool,
                )

            self.error_file = False
        except Exception as err:
            print('add_file __41', err)
            self.error_file = True

    def add_link(self):
        try:
            if len(self.request['link']) != 0:
                self.request_link = self.request['link']
                # получаем фавикон
                link_favicon = self.take_favicon()
                # получаем последнюю букву из ссылки
                request_link_first_letter = self.request['link'].split('://')[-1][0:1].upper()
            else:
                self.request_link = self.request['linkDesc']
                # получаем фавикон
                link_favicon = self.take_favicon()
                # получаем последнюю букву из ссылки
                request_link_first_letter = self.request['linkDesc'].split('://')[-1][0:1].upper()

            if len(self.request['linkDesc']) != 0:
                request_link_desc = self.request['linkDesc']
            else:
                request_link_desc = self.request['link']

            try:
                if self.request['link_id'] != '':
                    self.link_id = int(self.request['link_id'])
            except Exception as err:
                print(f'нет "link_id" или не верный формат: {self.link_id}', err)
                self.error_link = True

            CardLink.objects.update_or_create(
                id=self.link_id,
                defaults={
                    'text': self.request_link,
                    'description': request_link_desc,
                    'first_letter': request_link_first_letter,
                    'favicon': link_favicon,
                    'card': Card.objects.get(id=self.request['card_id']),
                },
                create_defaults={
                    'text': self.request_link,
                    'description': request_link_desc,
                    'first_letter': request_link_first_letter,
                    'favicon': link_favicon,
                    'card': Card.objects.get(id=self.request['card_id']),
                }
            )

            self.error_link = False
        except Exception as err:
            print('add_link __95', err)
            self.error_link = True

    def take_favicon(self):
        try:
            parsed_url = urllib3.util.parse_url(self.request_link)
        except Exception as err:
            print(err)
            return None

        http = urllib3.PoolManager()

        try:
            response = http.request('GET', self.request_link)
        except Exception as err:
            print(err)
            return None

        soup = BeautifulSoup(response.data, features="html.parser")

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
        except Exception as err:
            print('41', err)
            return None


# add_error = AddFileAndLink(request.data)
# print(f'error __69 => {add_error}')
#
# if add_error.error_file and add_error.error_link:
#     return Response(False, status=status.HTTP_404_NOT_FOUND)
# return Response(card_data, status=status.HTTP_200_OK)