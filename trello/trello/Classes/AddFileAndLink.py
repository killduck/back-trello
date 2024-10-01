from ..models import Card, CardFile, CardLink, ImageExtension
from ..serializers import ImageExtensionSerializer

import urllib3
from bs4 import BeautifulSoup

class AddFileAndLink:
    request = None
    image_bool = False
    img_extensions = None
    card_id = None
    link_id = None
    request_link_first_letter = None
    icon_link = None
    request_link = None
    request_link_desc = None
    link_favicon = None
    error_file = None
    error_link = None

    def __init__(self, request):
        try:
            self.request = request.data

            if self.request['card_id']:
                self.card_id = Card.objects.get(id=self.request['card_id'])

            if len(self.request['file']) > 0:
                print(f'25__ file => {self.request['file']}')
                self.add_file()

            if len(self.request['link']) != 0 or len(self.request['linkDesc']) != 0:
                print(f'29__ link => {self.request['link']}, linkDesc => {self.request['linkDesc']}')
                self.add_link()

        except Exception as ex:
            print('24__ request.data', ex)
            self.error_file = True
            return

    def add_file(self):
        try:
            file_list = self.request.getlist('file')
            self.img_extensions = ImageExtensionSerializer(ImageExtension.objects.all(), many=True).data

            for file in file_list:
                print(f'36__ => {file.name.split('.')[-1]}')
                request_file_extension = file.name.split('.')[-1]

                for img_extension in self.img_extensions:
                    if request_file_extension == img_extension['type']:
                        print(f'41__ {request_file_extension, img_extension['type']}')
                        self.image_bool = True

                CardFile.objects.create(
                    card=self.card_id,
                    name=file.name,
                    size=file.size,
                    extension=request_file_extension,
                    file_url=file,
                    image=self.image_bool,
                )

            self.error_file = False
        except Exception as ex:
            print('55__ add_file', ex)
            self.error_file = True

    def add_link(self):
        try:
            if len(self.request['link']) != 0:
                self.request_link = self.request['link']
                # получаем favicon
                self.link_favicon = self.take_favicon()
                # получаем последнюю букву из ссылки
                self.request_link_first_letter = self.request['link'].split('://')[-1][0:1].upper()
            else:
                self.request_link = self.request['linkDesc']
                # получаем favicon
                self.link_favicon = self.take_favicon()
                # получаем последнюю букву из ссылки
                self.request_link_first_letter = self.request['linkDesc'].split('://')[-1][0:1].upper()

            if len(self.request['linkDesc']) != 0:
                self.request_link_desc = self.request['linkDesc']
            else:
                self.request_link_desc = self.request['link']

            try:
                if self.request['link_id'] != '':
                    self.link_id = int(self.request['link_id'])
            except Exception as ex:
                print(f'нет "link_id" или не верный формат: {self.link_id}', ex)
                self.error_link = True

            CardLink.objects.update_or_create(
                id=self.link_id,
                defaults={
                    'text': self.request_link,
                    'description': self.request_link_desc,
                    'first_letter': self.request_link_first_letter,
                    'favicon': self.link_favicon,
                    'card': self.card_id,
                },
                create_defaults={
                    'text': self.request_link,
                    'description': self.request_link_desc,
                    'first_letter': self.request_link_first_letter,
                    'favicon': self.link_favicon,
                    'card': self.card_id,
                }
            )

            self.error_link = False
        except Exception as ex:
            print('105__ add_link', ex)
            self.error_link = True

    def take_favicon(self):
        try:
            parsed_url = urllib3.util.parse_url(self.request_link)
        except Exception as ex:
            print(ex)
            return None

        http = urllib3.PoolManager()

        try:
            response = http.request('GET', self.request_link)
        except Exception as ex:
            print(ex)
            return None

        soup = BeautifulSoup(response.data, features="html.parser")

        if soup.find("link", rel="shortcut icon"):
            icon_link = soup.find("link", rel="shortcut icon")
        else:
            icon_link = soup.find("link", rel="icon")
        # print(f'129__ {icon_link}')

        try:
            icon = icon_link['href']
            if parsed_url.scheme[0:4] == icon[0:4]:
                favicon = f'{icon}'
            else:
                favicon = f'{parsed_url.scheme}://{parsed_url.host}{icon}'
            # print(f'138__ {favicon}')
            if favicon:
                return favicon
            return None
        except Exception as ex:
            print(f'143__ {ex}')
            return None
