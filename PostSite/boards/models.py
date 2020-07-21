from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Board(models.Model):
    name= models.CharField(max_length=30,unique=True)
    description=models.CharField(max_length=200)
    

# One way to create a relationship between the models is by using the ForeignKey field. 
# It will create a link between the models and create a proper relationship at the database level. 
# The ForeignKey field expects a positional parameter with the reference to the model it will relate to.


#Topic model, the board field is a ForeignKey to the Board model. 
#It is telling Django that a Topic instance relates to only one Board instance. 
#The related_name parameter will be used to create a reverse relationship where the Board instances will have access a list of Topic instances that belong to it.
#For example, in the Topic model, the board field is a ForeignKey to the Board model. It is telling Django that a Topic instance relates to only one Board instance. The related_name parameter will be used to create a reverse relationship where the Board instances will have access a list of Topic instances that belong to it.
class Topic(models.Model):
    subject=models.CharField(max_length=255)
    last_updated=models.DateTimeField(auto_now_add=True)
    board=models.ForeignKey(Board,on_delete=models.CASCADE, related_name='topics')
    starter=models.ForeignKey(User,on_delete=models.CASCADE, related_name='topics')
    

#This will instruct Django to set the current date and time when a Post object is created(auto_now_add)
class Post(models.Model):
    message=models.TextField(max_length=4000)
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='posts')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='+')
   

