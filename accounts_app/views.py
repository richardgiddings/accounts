from django.shortcuts import render
from .models import Account

def transaction_screen(request):

    accounts = Account.objects.all()

    return render(request, 
                  template_name='accounts_app/transaction_screen.html',
                  context={'accounts': accounts})