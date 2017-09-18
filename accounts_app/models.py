from django.db import models
from django.utils.dateformat import format
from django.conf import settings

class Account(models.Model):

    name = models.IntegerField(primary_key=True)
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=200)
    email = models.EmailField()

    def __str__(self):
        return str(self.name)

class Transaction(models.Model):

    datetime_of_transaction = models.DateTimeField(auto_now_add=True, blank=True)
    from_account = models.IntegerField()
    to_account = models.IntegerField()
    amount_transferred = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return format(self.datetime_of_transaction, settings.DATETIME_FORMAT)