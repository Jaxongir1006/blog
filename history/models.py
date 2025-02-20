from django.db import models

# Create your models here.

class History(models.Model):
    user = models.ForeignKey('user.Profile', on_delete=models.CASCADE)
    blog =  models.ForeignKey('blogging.Blog', on_delete=models.CASCADE)

class Saved(models.Model):
    user = models.ForeignKey('user.Profile', on_delete=models.CASCADE)
    blog =  models.ForeignKey('blogging.Blog', on_delete=models.CASCADE)
