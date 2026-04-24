from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)


    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username