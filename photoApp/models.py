from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField 

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture =CloudinaryField('profile_picture')


    def __str__(self):
        return self.user.username

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = CloudinaryField('image')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')

    def __str__(self):
        return f"{self.user.username} likes {self.photo.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.photo.title}"