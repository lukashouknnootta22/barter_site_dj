from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal
from .forms import SignUpForm, AdForm, ExchangeProposalForm
from django.utils import timezone

class SignUpTest(TestCase):
    # Тесты регистрации
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')

    def test_signup_form_valid(self):
        """Регистрация пользователя"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_form_invalid(self):
        """Неверная регистрация пользователя"""
        data = {
            'username': 'testuser',
            'email': 'invalid_email',  # Некорректный email
            'password1': 'securepassword123',
            'password2': 'differentpassword'  # Пароли не совпадают
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())

class LoginTest(TestCase):
    # Тесты авторизации
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='securepassword123')

    def test_login_success(self):
        """Авторизация пользователя"""
        data = {'username': 'testuser', 'password': 'securepassword123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_failure(self):
        """Неверная авторизация пользователя"""
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

class CreateAdTest(TestCase):
    # Тесты для Объявлений
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='securepassword123')
        self.client.login(username='testuser', password='securepassword123')
        self.create_ad_url = reverse('create_ad')

    def test_create_ad_success(self):
        """Тест создания Объявления"""
        data = {
            'title': 'Test Ad',
            'description': 'Test',
            'category': 'E',
            'condition': 'N'
        }
        response = self.client.post(self.create_ad_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title='Test Ad').exists())

    def test_create_ad_failure(self):
        """Тест неверного создания Объявления"""
        data = {
            'title': '',  # Пустое название
            'description': 'Test',
            'category': 'E',
            'condition': 'N'
        }
        response = self.client.post(self.create_ad_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Ad.objects.filter(description='Test').exists())

class CreateExchangeProposalTest(TestCase):
    # Тесты для Предложений обмена
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='securepassword123')
        self.user2 = User.objects.create_user(username='user2', password='securepassword123')
        self.ad_receiver = Ad.objects.create(
            title='Receiver Ad',
            description='Test',
            category='E',
            condition='N',
            user=self.user2
        )
        
        self.client.login(username='user1', password='securepassword123')
        self.create_exchange_proposal_url = reverse('create_exchange_proposal', args=[self.ad_receiver.id])

    def test_create_exchange_proposal_success(self):
        """Тест создания Предложения обмена"""
        ad_sender = Ad.objects.create(
            title='Sender Ad',
            description='This is a sender ad',
            category='E',
            condition='N',
            user=self.user1
        )
        data = {
            'ad_sender': ad_sender.id,
            'comment': 'I want to exchange this item',
            'ad_receiver': self.ad_receiver.id
        }
        response = self.client.post(self.create_exchange_proposal_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ExchangeProposal.objects.filter(comment='I want to exchange this item').exists())

    def test_create_exchange_proposal_failure(self):
        """Тест неверного создания Предложения обмена"""
        data = {
            'ad_sender': '',  # Пустой отправитель
            'comment': 'I want to exchange this item'
        }
        response = self.client.post(self.create_exchange_proposal_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ExchangeProposal.objects.filter(comment='I want to exchange this item').exists())


