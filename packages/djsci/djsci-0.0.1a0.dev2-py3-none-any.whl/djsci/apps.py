from django.apps import AppConfig


class DjsciConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "djsci"

import os
from pathlib import Path
from django.utils.autoreload import autoreload_started

# Watch .conf files
def watch_extra_files(sender, *args, **kwargs):
    watch = sender.extra_files.add
    watch_dir = sender.watch_dir
    # List of file paths to watch
    watch_list = [
        './local_notebooks/',
    ]
    for file in watch_list:
    #     if os.path.exists(file): # personal use case
    #         watch(Path(file))
        watch_dir(Path(file), "**/*")


autoreload_started.connect(watch_extra_files)