from django.db import models

# Create your models here.

class Scrap(models.Model):
    id = models.AutoField(primary_key=True)
    #name = models.FileField(upload_to="db/name")
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    #csv = models.FileField(upload_to="db/csv", max_length=200)
    csv = models.CharField(max_length=100)
    
    def __str__(self):
        return self.author
