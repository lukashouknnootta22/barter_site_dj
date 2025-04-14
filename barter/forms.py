from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class SignUpForm(UserCreationForm):
	# Форма для регистрации пользователей.
	
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
		labels = {'username':'Логин'}

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError(f'Пользователь с данным email уже существует')
		return email

class UserProfileForm(forms.ModelForm):
	# Форма для редактирования пользователей.
	username = forms.CharField(label='Логин', widget=forms.TextInput())
	new_password1 = forms.CharField(label='Новый пароль', required=False, widget=forms.PasswordInput(attrs={'class':'form-input'}))
	new_password2 = forms.CharField(label='Подтверждение нового пароля', required=False, widget=forms.PasswordInput(attrs={'class':'form-input'}))

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']

	def clean(self):
		cleaned_data = super().clean()
		new_password1 = cleaned_data['new_password1']
		new_password2 = cleaned_data['new_password2']

		if new_password1 and new_password1 != new_password2:
			raise forms.ValidationError('Введённые пароли не совпадают')
		return cleaned_data

	def save(self):
		user = super().save(commit=False)
		new_password = self.cleaned_data.get('new_password1')
		if new_password:
			user.set_password(new_password)
			user.save()
		return user

class AdForm(forms.ModelForm):
	# Форма для создания объявления.
	class Meta:
		model = Ad
		fields = ['title', 'description', 'image_url', 'category', 'condition']


class ExchangeProposalForm(forms.ModelForm):
	# Форма для предложения обмена.
	class Meta:
		model = ExchangeProposal
		fields = ['ad_sender', 'ad_receiver', 'comment']
		widgets = {
		'ad_sender':forms.HiddenInput(),
		'ad_receiver':forms.HiddenInput(),
		}

	def clean(self):
		cleaned_data = super().clean()
		ad_sender = cleaned_data.get('ad_sender')
		ad_receiver = cleaned_data.get('ad_receiver')
		if ad_sender == ad_receiver:
			raise forms.ValidationError('Нельзя отправить предложение обмена самому себе.')
		if not ad_sender or not ad_receiver:
			raise forms.ValidationError('Объявление отправителя или получателя не найдено.')
		return cleaned_data