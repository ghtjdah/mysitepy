from django.db import models

# Create your models here.

class Guestbook(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    message = models.TextField(blank=True)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Guestbook(%s, %s, %s)"%(self.name,self.message,self.reg_date)