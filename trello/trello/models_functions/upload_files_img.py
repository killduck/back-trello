# lets us explicitly set upload path and filename
def upload_to_images(instance, filename):
    return f'images/{filename}'.format(filename=filename)

def upload_to_files(instance, filename):
    return f'files/{filename}'.format(filename=filename)