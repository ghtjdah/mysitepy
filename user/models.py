from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'user'

    def __str__(self):
        return "User(%s, %s, %s, %s)"%(self.name,self.email,self.password,self.gender)