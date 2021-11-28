from django.db import models
from django.contrib.auth.models import User


class FacultyInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    first_name=models.CharField(max_length=20,null=True,blank=True)
    last_name=models.CharField(max_length=20,null=True, blank=True)
    picture = models.ImageField(upload_to = 'faculty_profile_pics', blank=True)

    def __str__(self):
        return self.user.first_name
    
    class Meta:
        verbose_name_plural = 'Faculty Info'