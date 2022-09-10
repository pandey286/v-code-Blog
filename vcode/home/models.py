from pyexpat import model
from sqlite3 import Timestamp
from django.db import models

# Create your models here.
# Database  --> Excel WorkBook
# Models In Django --> Table ---> Sheet

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=100)
    content = models.TextField()
    Timestamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return 'Message from ' + self.name + ' - ' + self.email
