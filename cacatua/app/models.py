# Create your models here.
from django.db import models
from django.utils.text import slugify

class Person(models.Model):
    name = models.CharField(max_length=50)
    birth = models.DateField()
    slug = models.SlugField()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
