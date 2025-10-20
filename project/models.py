from django.db import models
import uuid
from users.models import Profile
# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000,null=True,blank=True)
    featured_image = models.ImageField(null=True,blank=True,default="default.jpg")
    tags = models.ManyToManyField('Tag',blank=True)
    demo_link = models.CharField(max_length=2000,null=True,blank=True)
    source_link = models.CharField(max_length=2000,null=True,blank=True)
    vote_count = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-vote_ratio','-vote_count','name']
    @property 
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()


        ratio = (upVotes/totalVotes)*100
        self.vote_count = totalVotes
        self.vote_ratio = ratio
        self.save()
    
    @property 
    def imageURL(self):
        try:
            url= self.featured_image.url
        except:
            url=''
        return url
    
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id',flat=True)
        return queryset
    
   

class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    VOTE_TYPE = (
        ('up','Up vote'),
        ('down','Down vote'),

    )
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.SET_NULL)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    body = models.TextField(max_length=2000,null=True,blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['owner','project']]
   
    def __str__(self):
        return self.value

        
       
