from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def __str__(self):
        return self.rec_name

class Meta:
        ordering=['rec_name']
        # name we use
        verbose_name="user"
class Receipe(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)
    rec_name=models.CharField(max_length=100)
    rec_desc=models.TextField()
    rec_image=models.ImageField(upload_to="receipe")
