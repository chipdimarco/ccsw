# 11-23-2018: Mozilla Tutorial Section 10
# Create your tests here.

import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookForm, BorrowBookForm

class BorrowBookFormTest(TestCase):
    def test_borrow_form_date_field_label(self):
        form = BorrowBookForm()
        self.assertTrue(form.fields['due_date'].label == None or form.fields['due_date'].label == 'due date')

    def test_borrow_form_date_field_help_text(self):
        form = BorrowBookForm()
        self.assertEqual(form.fields['due_date'].help_text, 'Standard Loan Period: 3 Weeks')

    def test_borrow_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = BorrowBookForm(data={'due_date': date})
        self.assertFalse(form.is_valid())

    def test_borrow_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = BorrowBookForm(data={'due_date': date})
        self.assertFalse(form.is_valid())

    def test_borrow_form_date_today(self):
        date = datetime.date.today()
        form = BorrowBookForm(data={'due_date': date})
        self.assertTrue(form.is_valid())
        
    def test_borrow_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form = BorrowBookForm(data={'due_date': date})
        self.assertTrue(form.is_valid())


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
        
    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())