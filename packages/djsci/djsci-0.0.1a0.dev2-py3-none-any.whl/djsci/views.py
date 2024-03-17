import os

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
import nbconvert
import nbformat
from nbformat.notebooknode import NotebookNode

from djsci.models import LocalNotebook, PrivateFile


def api_root(request: HttpRequest) -> JsonResponse:
    return JsonResponse("djsci_api_root", safe=False)


def sync_get_file(name_id: str) -> bytes:
    try:
        private_file = PrivateFile.objects.get(name=name_id).file
    except:
        private_file = PrivateFile.objects.get(id=name_id).file

    with private_file.open() as open_file:
        sync_file = open_file.read()

    return sync_file


def convert_ipynb_to_python(sync_file: bytes) -> str:
    notebook_node = nbformat.reads(sync_file, as_version=4)
    notebook_python = nbconvert.PythonExporter().from_notebook_node(notebook_node)[0]

    return notebook_python


def sync_exec(
    request: HttpRequest, sync_file: bytes | str
) -> (
    # not sure how else to allow any json :
    dict
    | list
    | str
    | int
    | float
    | bool
    | None
):
    # not sure why locals() doesn't work :

    exec(sync_file, globals())  # , locals())

    # if 'djsci_handler' not in locals() and 'djsci_handler' not in globals():
    #     djsci_handler = lambda request: {'message': 'djsci_handler not defined'}

    return djsci_handler(request)


def sync_py(request: HttpRequest, name_id: str) -> JsonResponse:
    sync_file = sync_get_file(name_id)
    djsci_handler_result = sync_exec(request, sync_file)

    return JsonResponse(djsci_handler_result, safe=False)


def sync_ipynb(request: HttpRequest, name_id: str) -> JsonResponse:
    sync_file = sync_get_file(name_id)
    notebook_python = convert_ipynb_to_python(sync_file)
    djsci_handler_result = sync_exec(request, notebook_python)

    return JsonResponse(djsci_handler_result, safe=False)


def async_ipynb(request: HttpRequest, name_id: str) -> JsonResponse:
    # sync_file = sync_get_file(name_id)
    # notebook_python = convert_ipynb_to_python(sync_file)
    # djsci_handler_result = sync_exec(request, notebook_python)

    return JsonResponse(djsci_handler_result, safe=False)


def nb_sync_get_file(name_id: str) -> bytes:
    try:
        private_file = LocalNotebook.objects.get(notebook=f'{LocalNotebook.notebook.field.upload_to}/{name_id}.ipynb').notebook
    except:
        private_file = LocalNotebook.objects.get(id=name_id).notebook

    with private_file.open() as open_file:
        sync_file = open_file.read()

    return sync_file


def ipynb_sync(request: HttpRequest, name_id: str) -> JsonResponse:
    sync_file = nb_sync_get_file(name_id)
    notebook_python = convert_ipynb_to_python(sync_file)
    djsci_handler_result = sync_exec(request, notebook_python)

    return JsonResponse(djsci_handler_result, safe=False)


def ipynb_async(request: HttpRequest, name_id: str) -> JsonResponse:
    sync_file = nb_sync_get_file(name_id)
    notebook_python = convert_ipynb_to_python(sync_file)
    djsci_handler_result = sync_exec(request, notebook_python)

    return JsonResponse(djsci_handler_result, safe=False)


import papermill
from nbconvert import HTMLExporter

def convert_ipynb_to_html(sync_file: bytes) -> str:
    notebook_node = nbformat.reads(sync_file, as_version=4)
    # notebook_python = nbconvert.PythonExporter().from_notebook_node(notebook_node)[0]
    nb = papermill.execute_notebook(notebook_node, None)

    html_exporter = HTMLExporter(template_name="classic")
    (body, resources) = html_exporter.from_notebook_node(nb)

    return body


def ipynb_exec(request: HttpRequest, name_id: str) -> JsonResponse:
    sync_file = nb_sync_get_file(name_id)
    notebook_html = convert_ipynb_to_html(sync_file)
    # djsci_handler_result = sync_exec(request, notebook_python)

    return HttpResponse(notebook_html)


import docker

docker_client = docker.from_env()

def ipynb_container(request: HttpRequest, name_id: str) -> JsonResponse:
    # sync_file = nb_sync_get_file(name_id)
    # notebook_html = convert_ipynb_to_html(sync_file)
    # # djsci_handler_result = sync_exec(request, notebook_python)

    docker_client.containers.run(
        'djsci_async',
        detach=True,
        environment={
            'DJSCI_IPYNB_NAME': name_id,
        },
        volumes={
            # 'djsci_data': {'bind': '/djsci_data', 'mode': 'ro'},
            # 'djsci_output': {'bind': '/output', 'mode': 'rw'},
            f'{os.getcwd()}/djsci_output': {'bind': '/djsci_output/', 'mode': 'rw'},
            f'{os.getcwd()}/djsci_data': {'bind': '/djsci_data/', 'mode': 'rw'},
            f'{os.getcwd()}/local_notebooks': {'bind': '/local_notebooks/', 'mode': 'rw'},
        },
    )

    return JsonResponse({'message': f'running container with {name_id}'})
