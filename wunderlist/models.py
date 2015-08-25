from django.db import models
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from django import forms
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super(Category, self).save(*args, **kwargs)


    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    #url = models.URLField()
    subtask = models.CharField(max_length=128)
    notes = models.TextField()
    dueDate = models.DateField()
    tags = TaggableManager(blank=True)
    #slug = models.SlugField(unique=True)
    taskDone = models.BooleanField(default=False)
    
    #def save(self, *args, **kwargs):
     #           self.slug = slugify(self.title)
      #          super(Item, self).save(*args, **kwargs)


    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=42)
    text = models.TextField()
    post = models.ForeignKey(Item)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text