# djsci : django_science :
## run jupyter notebooks in django

add djsci to your django project to be able to run jupyter notebooks or any python file via an api



this `README` assumes general familiarity with `python`, `django` & `jupyter notebooks`

[# TODO :  add detailed tutorial]

this MVP framework was created using `python 3.10`

install :
```
pip install djsci

or

python -m pip install djsci
```

add `djsci` to `INSTALLED_APPS` in `settings.py` :
```
....

INSTALLED_APPS = [
    ....
    'djsci',
    ....
]

....
```

import and add `djsci_urls` to `urlpatterns` in `settings.py` :
```
....

from djsci.urls import djsci_urls

....

urlpatterns = [

    ....

] + djsci_urls

....
```

apply migrations for `djsci` :
```
python ./manage.py migrate djsci
```

run django dev server :
```
python ./manage.py runserver
```

login to the admin :
```
http://127.0.0.1:8000/admin/
```

once authenticated point browser to the `djsci root` :
```
http://127.0.0.1:8000/djsci/
```

you should see :
```
"djsci_api_root"
```

# run a simple jupyter notebook via django api :

create a jupyter notebook file named `heyo_multiverse.ipynb` with a function named `djsci_handler` in a cell :
```
def djsci_handler(request):
    heyo_multiverse = 'heyo multiverse !!!! [notebook]'
    print(heyo_multiverse)
    return heyo_multiverse
```

navigate in the django admin to add a `private file` :
```
http://127.0.0.1:8000/admin/djsci/privatefile/add/
```

upload your `heyo_multiverse.ipynb` file and enter name `heyo_multiverse_ipynb` in the form [leave everything else blank]

click save

then navigate your browser to this `url` :  [you must be authenticated]

```
http://127.0.0.1:8000/djsci/sync_ipynb/heyo_multiverse_ipynb/

or

http://127.0.0.1:8000/djsci/sync_ipynb/<PRIVATE_FILE_SHORT_UUID>/

# example :
# http://127.0.0.1:8000/djsci/sync_ipynb/3DLCCaNeVdhvaSRPABoee8/
```

you should see :
```
"heyo multiverse !!!! [notebook]"
```

# run a simple python file via django api :

create a python file named `heyo_multiverse.py` with a function named `djsci_handler` :
```
def djsci_handler(request):
    heyo_multiverse = 'heyo multiverse !!!! [python]'
    print(heyo_multiverse)
    return heyo_multiverse
```

navigate in the django admin to add a `private file` :
```
http://127.0.0.1:8000/admin/djsci/privatefile/add/
```

upload your `heyo_multiverse.py` file and enter name `heyo_multiverse_py` in the form [leave everything else blank]

click save

then navigate your browser to this `url` :  [you must be authenticated]
```
http://127.0.0.1:8000/djsci/sync_py/heyo_multiverse_py/

or

http://127.0.0.1:8000/djsci/sync_py/<PRIVATE_FILE_SHORT_UUID>/

# example :
# http://127.0.0.1:8000/djsci/sync_py/oZVULxKrCfRhYGF4WUckC2/
```

you should see :
```
"heyo multiverse !!!! [python]"
```

## future :

too many ideas including but not limited to :

```
• add token authentication for api access [saying this first because it is painfully obvious it is needed ;  though maybe not drf ?  which is why it has not been added yet]

• make this framework easy to install and use as a stand alone app or as part of a django project

• run notebooks asynchronously

• run notebooks in containers [containerd/lima]

• run and access uploaded notebooks in a running jupyter notebook instance

• provide an easy way to chain a series of notebooks for data pipelining etl model training inference etc.

• easliy move notebooks from local enviroment to development environments and add a way to export notebooks to check in to version control before releasing and deploying to production environments

• develop python package that can be used in a notebook that integrates with the backend

• easily deploy using zappa and to aws other ways [integration with other systems/services as well]

• look for the right balance between allowing ease of use and accessibility and insist on ensuring rock solid security

• always support easy full end to end testing locally and then deploy to and run in scalable andor serverless cloud services
```

## disclaimers :

be careful how you use this framework

secure and restrict access to uploaded files because they are run via the django instance

running code from files not committed and merged through a peer review process in publicly accessible systems comes with significant risks that can be addressed and mitigated if handled correctly

it is the goal of the project to directly address and put on the roadmap items related to these concerns
