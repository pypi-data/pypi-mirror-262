from django.urls import path, re_path
from django.views.static import serve
from django.contrib.auth.decorators import login_required

from djsci import views
from djsci.models import LocalNotebook


DJSCI_API_ROOT = "djsci"


djsci_urls = [
    re_path(rf"{DJSCI_API_ROOT}/?$", views.api_root, name="api_root"),
    re_path(
        rf"{DJSCI_API_ROOT}/sync_py/(?P<name_id>\w+)/?$",
        login_required(views.sync_py),
        name="sync_py",
    ),
    re_path(
        rf"{DJSCI_API_ROOT}/sync_ipynb/(?P<name_id>\w+)/?$",
        login_required(views.sync_ipynb),
        name="sync_ipynb",
    ),
    re_path(
        r"^private_files/(?P<path>.*)$",
        serve,
        {"document_root": "private_files"},
    ),
    re_path(
        rf"{DJSCI_API_ROOT}/ipynb_sync/(?P<name_id>\w+)/?$",
        login_required(views.ipynb_sync),
        name="ipynb_sync",
    ),
    re_path(
        rf"{DJSCI_API_ROOT}/ipynb_exec/(?P<name_id>\w+)/?$",
        login_required(views.ipynb_exec),
        name="ipynb_exec",
    ),
    re_path(
        rf"{DJSCI_API_ROOT}/ipynb_container/(?P<name_id>\w+)/?$",
        login_required(views.ipynb_container),
        name="ipynb_container",
    ),
]

import sys
import os

if 'runserver' in sys.argv:

#     print('OXOXOXOX urls runserver')
    
    print(
        'OXOXOXOX urls runserver',
        [file for file in os.listdir(LocalNotebook.notebook.field.upload_to) if file.endswith('.ipynb')]
    )

    for notebook in [file for file in os.listdir(LocalNotebook.notebook.field.upload_to) if file.endswith('.ipynb')]:

        print('notebook LOOP : ', notebook)

        if not LocalNotebook.objects.filter(notebook=f'{LocalNotebook.notebook.field.upload_to}/{notebook}').exists():

            temp = LocalNotebook()

            temp.notebook.name = f'{LocalNotebook.notebook.field.upload_to}/{notebook}'

            temp.save()

            print('notebook CREATED : ', f'{LocalNotebook.notebook.field.upload_to}/{notebook}')

#         # with open(f'./local_notebooks/{notebook}') as nb:
#         #     nb = nb.read()
#         print(f'notebook : ./local_notebooks/{notebook}')

#         # print(f'notebook : ./local_notebooks/{notebook}')


    for db_notebook in LocalNotebook.objects.all():

        print('db_notebook : ', db_notebook)

        print(
            'db_notebook.notebook.storage.exists(db_notebook.notebook.name) : ',
            db_notebook.notebook.storage.exists(db_notebook.notebook.name),
        )

        if not db_notebook.notebook.storage.exists(db_notebook.notebook.name):

            db_notebook.delete()

            print('DELETED : ', db_notebook)

    print(
        'LocalNotebook.objects.all : ',
        [file for file in LocalNotebook.objects.all()]
    )
        
#     print(
#         [file.notebook for file in LocalNotebook.objects.all() if file.notebook.name.endswith('.ipynb')]
#     )

#     print(
#         'LocalNotebook.objects.get',
#         LocalNotebook.objects.get(notebook='heyo_multiverse.ipynb')
#     )
        
    # fp = f'{LocalNotebook.notebook.field.upload_to}/heyo_auto.ipynb'

    # print('fp : ', fp)

    # n = LocalNotebook.objects.get(notebook=fp)

#     print(
#         'LocalNotebook contents : ',
#         n.notebook.name # file.read().decode()
#     )

    print(
        'os.getcwd()',
        os.getcwd(),
    )

    print(
        'os.listdir()',
        os.listdir(),
    )

    # from djsci.models import LocalNotebook
    # n = LocalNotebook.objects.get(notebook=f'{LocalNotebook.notebook.field.upload_to}/heyo_multiverse_HhQBuhg.ipynb')
    # n_read = n.notebook.file.read().decode()

    # print('n_read : ', n_read)

    # print('LocalNotebook.notebook.field.upload_to : ', LocalNotebook.notebook.field.upload_to)


#     print(
#         'LocalNotebook.notebook.field.upload_to : ',
#         LocalNotebook.notebook.field.upload_to,
#     )
    

# print('OXOXOXOX urls runserver os.getcwd() : ', os.getcwd())
