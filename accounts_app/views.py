from django.shortcuts import render
from .models import Account, Transaction
from .forms import PaymentForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

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

def payment(request):
    """
    Make a payment screen
    """
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            from_account = data['from_account']
            to_account = data['to_account']
            amount_transferred = data['amount_transferred']

            if from_account == to_account:
                messages.error(request, 'Cannot transfer to same account.')
                return render(request, template_name='accounts_app/payment.html', 
                              context={ 'form': form })

            # get from_account and try and take amount off
            from_account_balance = from_account.balance
            from_account.balance = from_account.balance - amount_transferred
            if from_account.balance >= 0:
                # adjust from_account 
                from_account.save()

                # adjust to account
                to_account.balance = to_account.balance + amount_transferred
                to_account.save()

                # save the transaction
                form.save()

                # Confirm success to user
                messages.info(request, 'Transfer was successful.')

                ##
                ## Send an email here to both accounts
                ##

            else:
                messages.error(request, 'Cannot transfer more than current balance, which is {}.'.format(from_account_balance))
                return render(request, template_name='accounts_app/payment.html', 
                              context={ 'form': form })
    else:
        form = PaymentForm()
    
    return render(request, template_name='accounts_app/payment.html', 
                  context={ 'form': form })