# Register your models here.
from django.contrib import admin
from .models import Person, Article
from .models import User

admin.site.register(Person)
admin.site.register(Article)
admin.site.register(User)
