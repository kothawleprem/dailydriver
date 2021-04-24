from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.
class Todo(models.Model):
    status_choices = [
        ('C','Completed'),
        ('P','Pending'),
    ]
    priority_choices = [
        ('1','1️⃣'),
        ('2','2️⃣'),
        ('3','3️⃣'),
        ('4','4️⃣'),
        ('5','5️⃣'),
        ('6','6️⃣'),
        ('7','7️⃣'),
        ('8','8️⃣'),
        ('9','9️⃣'),
        ('10','🔟')
    ]
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=2, choices = status_choices)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=2, choices = priority_choices)

class Profile(models.Model):
    category_choices = [
        ('General' , 'General'),
        ('Business' , 'Business'),
        ('Entertainment' , 'Entertainment'),
        ('Health' , 'Health'),
        ('Science' , 'Science'),
        ('Sports' , 'Sports'),
        ('Technology' , 'Technology'),

    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=25,choices=category_choices,default=category_choices[0][0])

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save()




