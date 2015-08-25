from django import forms
from wunderlist.models import Item, Category, Comment
from django.forms import ModelForm
from taggit.forms import *

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']        

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    subtask = forms.CharField(max_length=128)
    notes = forms.CharField(widget = forms.Textarea)
    dueDate = forms.DateField(required=False,widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    tags = TagField(required=False)
    taskDone = forms.BooleanField(required=False)
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Item

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        #exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        fields = ('category', 'title', 'subtask', 'notes','dueDate','tags')