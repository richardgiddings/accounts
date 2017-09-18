from django.shortcuts import render
from .models import Account, Transaction
from django.db.models import Q

def transaction_screen(request):

    accounts = Account.objects.all()

    return render(request, 
                  template_name='accounts_app/transaction_screen.html',
                  context={'accounts': accounts})

def view_account(request, account_number):

    account = Account.objects.get(pk=account_number)

    transactions = Transaction.objects.filter(Q(from_account=account_number) | 
                                              Q(to_account=account_number))
    transactions = transactions.order_by('-datetime_of_transaction')

    return render(request, template_name='accounts_app/account.html',
                  context={ 'account': account, 'transactions': transactions })