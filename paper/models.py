from django.db import models

# Create your models here.


class Person(models.Model):
    username = models.CharField(max_length=120)
    clntId = models.CharField(max_length=120)
    paper_id = models.IntegerField(blank=True)

    def __str__(self):
        return self.username
