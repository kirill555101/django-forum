from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage


from main import models


def paginate(resources, page, resources_per_page):
    paginator = Paginator(resources, resources_per_page)
    return paginator.get_page(page)


def get_paginated_max_pax(resources, resources_per_page):
    paginator = Paginator(resources, resources_per_page)
    return paginator.num_pages


def save_file(file):
    path = '/static/users_avatar/default.png'

    if file is not None:
        fs = FileSystemStorage(location='/static/users_avatar/')
        filename = fs.save(file.name, file)
        path = '/static/users_avatar/' + file.name

    return path
