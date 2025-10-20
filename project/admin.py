from django.contrib import admin
from .models import Review,Project,Tag

# Register your models here.

admin.site.register([Review,Project,Tag])