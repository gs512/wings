from django.contrib import admin
from django.db.models import get_app, get_models
# Register your models here.
from library.models import *

for model in get_models(get_app("library")):
	admin.site.register(model)
