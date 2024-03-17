# djsci settings to be imported into django settings

from djsci.utils import (
    djsci_base_dir,
    djsci_setup,
)

djsci_setup(setup=False)

DJSCI_MODE = 'LOCAL'

DJSCI_INSTALLED_APPS = [
    'django_extensions',
]

def add_djsci_installed_apps(installed_apps):
    for app in DJSCI_INSTALLED_APPS:
        if app not in installed_apps:
            installed_apps.append(app)

SHELL_PLUS_DONT_LOAD = ['*']
