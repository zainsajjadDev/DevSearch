from django import forms
from django.forms import ModelForm
from .models import Profile,Skill,Message

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'profile_img': forms.FileInput(attrs={'class': 'input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})

class SkillForm(ModelForm):

    class Meta:
        model = Skill
        exclude = ['owner']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'input'})    

class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = ['name', 'email','subject','body']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'input'})    