from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,)
    last_name = models.CharField(max_length=255,)

    def __str__(self):

        return self.user.username

class Address(models.Model):

    STATE_CHOICES = [('KL','Kerala'),('TN','Tamilnadu'),('AP','Andrapradesh'),('KA','Karnataka'),('MA','Maharashtra'),('DL','Delhi')]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    state = models.CharField(max_length=2,choices=STATE_CHOICES)
    street1 = models.CharField(max_length=255, blank=True, null=True)
    street2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    post_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):

        return self.user.username
