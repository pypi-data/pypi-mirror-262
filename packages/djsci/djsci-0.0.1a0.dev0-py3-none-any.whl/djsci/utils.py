import os

import django


def djsci_setup(setup=True):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    if setup:
        django.setup()


def djsci_base_dir(base_dir=None):

    if base_dir is not None:
        os.chdir(base_dir)
