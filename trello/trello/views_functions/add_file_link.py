from .take_favicon import take_favicon
from ..models import Card, CardFile, CardLink, ImageExtension
from ..serializers import ImageExtensionSerializer


def add_file(request):

    image_bool = False
    img_extensions = ImageExtensionSerializer(ImageExtension.objects.all(), many=True).data

    try:
        file_list = request.getlist('file')
        for file in file_list:
            print('78__>>>', file.name.split('.')[-1])
            request_file_extension = file.name.split('.')[-1]

            for img_extension in img_extensions:
                if request_file_extension == img_extension['type']:
                    print(f'89__ {request_file_extension, img_extension['type']}')
                    image_bool = True

            CardFile.objects.create(
                card=Card.objects.get(id=request['card_id']),
                name=file.name,
                size=file.size,
                extension=request_file_extension,
                file_url=file,
                image=image_bool,
            )

        return False
    except Exception as err:
        print('add_file __26', err)
        return True


def add_link(request):

    link_id = None
    request_link_first_letter = None

    try:
        if len(request['link']) != 0:
            request_link = request['link']
            # получаем фавикон
            link_favicon = take_favicon(request_link)
            # получаем последнюю букву из ссылки
            request_link_first_letter = request['link'].split('://')[-1][0:1].upper()
        else:
            request_link = request['linkDesc']
            # получаем фавикон
            link_favicon = take_favicon(request_link)
            # получаем последнюю букву из ссылки
            request_link_first_letter = request['linkDesc'].split('://')[-1][0:1].upper()

        if len(request['linkDesc']) != 0:
            request_link_desc = request['linkDesc']
        else:
            request_link_desc = request['link']

        try:
            if request['link_id'] != '':
                link_id = int(request['link_id'])
        except Exception as err:
            print(f'нет "link_id" или не верный формат: {link_id}', err)
            return True

        CardLink.objects.update_or_create(
            id=link_id,
            defaults={
                'text': request_link,
                'description': request_link_desc,
                'first_letter': request_link_first_letter,
                'favicon': link_favicon,
                'card': Card.objects.get(id=request['card_id']),
            },
            create_defaults={
                'text': request_link,
                'description': request_link_desc,
                'first_letter': request_link_first_letter,
                'favicon': link_favicon,
                'card': Card.objects.get(id=request['card_id']),
            }
        )

        return False
    except Exception as err:
        print('add_link __26', err)
        return True
