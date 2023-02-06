from django.db import models

# Create your models here.
class CommonModel(models.Model):
    """Common momdel definition"""

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        abstract = True    