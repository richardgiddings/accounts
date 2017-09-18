from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Account, Transaction

class ViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):        
        # add some accounts
        cls.account1 = Account.objects.create(
            name=12345678, balance=100, email='mail1@test.com'
        )
        cls.account2 = Account.objects.create(
            name=23456789, email='mail1@test.com'
        )

    def test_transaction_screen(self):
        """
        Test the transaction screen
        """
        response = self.client.get(
            reverse('transaction_screen')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_app/transaction_screen.html')

        self.assertContains(response, '12345678')
        self.assertContains(response, '23456789')

    def test_view_account(self):
        """
        Test that the view account screen shows transactions
        """

        # create a couple of tranasctions
        transaction1 = Transaction.objects.create(
            from_account=self.account1, to_account=self.account2, 
            amount_transferred=100
        )
        transaction2 = Transaction.objects.create(
            from_account=self.account2, to_account=self.account1, 
            amount_transferred=6
        )

        # test the state of the screen
        response = self.client.get(
            reverse('view_account', kwargs={'account_number': self.account1})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_app/account.html')

        self.assertContains(response, 'Transactions for account number 12345678')
        self.assertContains(response, 'Current balance: 100.00')
        self.assertContains(response, '&#45;100.00')
        self.assertContains(response, 'From 12345678 to 23456789')
        self.assertContains(response, '6.00')
        self.assertContains(response, 'From 23456789 to 12345678')

    def test_payment_screen_initial(self):
        response = self.client.get(
            reverse('payment')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts_app/payment.html')

        self.assertContains(response, 'Go back to transaction screen')
        self.assertContains(response, 'From account')
        self.assertContains(response, 'To account')
        self.assertContains(response, 'Amount transferred')

    def test_payment_failure_accounts_the_same(self):
        response = self.client.get(
            reverse('payment')
        )
        form = response.context['form']
        data = form.initial
        data['from_account'] = self.account1
        data['to_account'] = self.account1
        data['amount_transferred'] = 100

        response = self.client.post(
            reverse('payment'), data, follow = True
        )

        # chek user gets a message saying they cannot transfer to same account
        self.assertContains(response, 'Cannot transfer to same account.')

    def test_payment_failure_not_enough_money(self):
        response = self.client.get(
            reverse('payment')
        )
        form = response.context['form']
        data = form.initial
        data['from_account'] = self.account1
        data['to_account'] = self.account2
        data['amount_transferred'] = 100.01

        response = self.client.post(
            reverse('payment'), data, follow = True
        )

        # chek user gets a message saying they cannot transfer to same account
        self.assertContains(response, 'Cannot transfer more than current balance')

    def test_payment_success(self):
        response = self.client.get(
            reverse('payment')
        )
        form = response.context['form']
        data = form.initial
        data['from_account'] = self.account1
        data['to_account'] = self.account2
        data['amount_transferred'] = 100.00

        response = self.client.post(
            reverse('payment'), data, follow = True
        )

        self.assertContains(response, 'Transfer was successful.')

        # check new balances
        account1 = Account.objects.get(pk=12345678)
        account2 = Account.objects.get(pk=23456789)

        self.assertEqual(account1.balance, 0.00)
        self.assertEqual(account2.balance, 300.00)

        # transactions?
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.get(from_account=self.account1, to_account=self.account2)
        self.assertEqual(transaction.amount_transferred, 100.00)
