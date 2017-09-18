from django.db import models

class Account(models.Model):

    name = models.IntegerField()
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    email = models.EmailField()