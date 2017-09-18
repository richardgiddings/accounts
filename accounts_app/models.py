from django.db import models

class Account(models.Model):

    name = models.IntegerField()
    balance = models.DecimalField(decimal_places=2)
    email = models.EmailField()