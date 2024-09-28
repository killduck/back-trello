

def add_file(request, img_extensions, image_bool):
    try:
        file_list = request.getlist('file')
        for file in file_list:
            print('78__>>>', file.name.split('.')[-1])
            extension =file.name.split('.')[-1]

            for img_extension in img_extensions:
                if extension == img_extension['type']:
                    print(f'89__ {extension, img_extension['type']}')
                    image_bool = True

            CardFile.objects.create(
                card=Card.objects.get(id=request['card_id']),
                name=file.name,
                size=file.size,
                extension=extension,
                file_url=file,
                image=image_bool,
            )
        errors = False
    except Exception as err:
        print(err)
        errors = True


def add_link():
    try:
        if len(request['link']) != 0 or len(request['linkDesc']) != 0:

            link_id = None
            request_link_first_letter = None

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
                link_id = int(request['link_id'])
            except Exception as err:
                print(err)
                errors = True

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
        errors = False
    except Exception as err:
        print(err)
        errors = True