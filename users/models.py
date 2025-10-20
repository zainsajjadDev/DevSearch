from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True , blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    username = models.CharField(max_length=200,null=True,blank=True)
    location = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True,unique=True)
    short_intro = models.CharField(max_length=200,null=True,blank=True)
    bio = models.TextField(max_length=2000,null=True,blank=True)
    profile_img = models.ImageField(null=True,blank=True,upload_to='profiles/',default='profiles/user-default.png')
    social_github = models.CharField(max_length=200,null=True,blank=True)
    social_linkedin = models.CharField(max_length=200,null=True,blank=True)
    social_youtube = models.CharField(max_length=200,null=True,blank=True)
    social_website = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)
    
    @property 
    def imageURL(self):
        try:
            url= self.profile_img.url
        except:
            url=''
        return url
     
class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(max_length=2000,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(f"{self.name} - {self.owner}")
    
class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True,blank=True)
    receipient = models.ForeignKey(Profile, on_delete=models.SET_NULL , null=True,blank=True,related_name="messages")
    name= models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=500,null=True,blank=True)
    body= models.TextField(null=True,blank=True)
    is_read = models.BooleanField(default=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['is_read','-created_at']

    def __str__(self):
        return self.subject