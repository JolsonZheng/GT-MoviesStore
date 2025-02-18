from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import PasswordReset

class PasswordResetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='old_password')
        self.password_reset = PasswordReset.objects.create(user=self.user, question='Test Question', answer='Test Answer')

    def test_password_reset_success(self):
        response = self.client.post(reverse('accounts.password_reset'), {
            'username': 'testuser',
            'question': 'Test Question',
            'answer': 'Test Answer',
            'new_password': 'new_password'
        })
        self.assertRedirects(response, reverse('accounts.login'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_password_reset_invalid_username(self):
        response = self.client.post(reverse('accounts.password_reset'), {
            'username': 'invaliduser',
            'question': 'Test Question',
            'answer': 'Test Answer',
            'new_password': 'new_password'
        })
        self.assertContains(response, 'The username, question, or answer is incorrect.')

    def test_password_reset_invalid_question(self):
        response = self.client.post(reverse('accounts.password_reset'), {
            'username': 'testuser',
            'question': 'Invalid Question',
            'answer': 'Test Answer',
            'new_password': 'new_password'
        })
        self.assertContains(response, 'The username, question, or answer is incorrect.')

    def test_password_reset_invalid_answer(self):
        response = self.client.post(reverse('accounts.password_reset'), {
            'username': 'testuser',
            'question': 'Test Question',
            'answer': 'Invalid Answer',
            'new_password': 'new_password'
        })
        self.assertContains(response, 'The username, question, or answer is incorrect.')

    def test_password_reset_invalid_form(self):
        response = self.client.post(reverse('accounts.password_reset'), {
            'username': '',
            'question': 'Test Question',
            'answer': 'Test Answer',
            'new_password': 'new_password'
        })
        self.assertContains(response, 'This field is required.')
