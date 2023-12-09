from django.contrib.auth.models import User
from django.db import models

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    
class FileShare(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    shared_by = models.ForeignKey(User, related_name='shared_by', on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, related_name='shared_with', on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)