from django.forms import ModelForm
from django import forms
from .models import Project,Review

class ProjectForm(ModelForm):
   class Meta:
      model = Project 
      fields = ["name","description",'featured_image',"demo_link","source_link","tags"]
      widgets ={
         'name':forms.TextInput(attrs={'class':'input'}),
         'description':forms.Textarea(attrs={'class':'input','row':4}),
         'featured_image':forms.FileInput(attrs={'class':'input'}),
         'tags':forms.CheckboxSelectMultiple(attrs={'class':'input'}),
         'demo_link':forms.TextInput(attrs={'class':'input'}),
         'source_link':forms.TextInput(attrs={'class':'input'}),
      }

class ReviewForm(ModelForm):
   class Meta:
      model = Review
      fields =  ['value','body']

      labels = {
         'value':'Place Your Vote',
         'body':'Add a comment to Project'
      }

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



   