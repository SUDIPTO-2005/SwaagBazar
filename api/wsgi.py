import os
from ecom.wsgi import application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecom.settings")

app = application