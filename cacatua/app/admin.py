# Register your models here.
from django.contrib import admin
from .models import Person, Article

admin.site.register(Person)
admin.site.register(Article)
