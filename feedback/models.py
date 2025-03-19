# feedback/models.py

from django.db import models

class ProductService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Feedback(models.Model):
    product_service = models.ForeignKey(ProductService, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    file_upload = models.FileField(upload_to='uploads/', blank=True, null=True)  # Add file upload field

    def __str__(self):
        return f'Feedback from {self.user_name} on {self.product_service}'
    
    
    
class Subscription(models.Model):
    user_name = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Subscription for {self.user_name}'
    