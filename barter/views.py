from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Ad, News, ExchangeProposal
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from .forms import AdForm, SignUpForm, UserProfileForm, ExchangeProposalForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm

@require_http_methods(['GET'])
def index(request):
	# Отображения главной страницы с новостями.
	latest_news = News.objects.all().order_by('-created_at')[:5] # Получение последних 5 новостей
	return render(request, 'barter/index.html', {'latest_news':latest_news})

@require_http_methods(['GET', 'POST'])
def signup(request):
	# Регистрация пользователей.
	if request.method == 'POST':
		signup_form = SignUpForm(request.POST)
		if signup_form.is_valid():
			try:
				user = signup_form.save()
				messages.success(request, 'Успешная регистрация')
				return redirect('login')
			except Exception as e:
				messages.error(request, 'Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.')
	else:
		signup_form = SignUpForm()
	return render(request, 'barter/signup.html', {'form': signup_form})

@require_http_methods(['GET', 'POST'])
def login(request):
	# Авторизация пользователей.
	if request.method == 'POST':
		login_form = AuthenticationForm(request, request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			user = authenticate(username=username, password=password)

			if user is not None:
				auth_login(request, user)
				messages.success(request, 'Успешная авторизация')
				return redirect('/')
		else:
			messages.error(request, 'Неверный логин или пароль. Повторите ввод.')
	else:
		login_form = AuthenticationForm()
	return render(request, 'barter/login.html', {'form':login_form})

@login_required
@require_http_methods(['GET'])
def logout_views(request):
	# Деавторизация
	logout(request)
	messages.success(request, 'Вы успешно вышли')
	return redirect('/')

@login_required
@require_http_methods(['GET'])
def profile(request):
	# Профиль пользователя со всеми его объявлениямию.	
	user_ads = Ad.objects.filter(user=request.user)
	return render(request, 'barter/profile.html', {
		'user': request.user,
		'user_ads': user_ads
    })

@login_required
@require_http_methods(['GET', 'POST'])
def edit_profile(request):
	# Изменение профиля
	if request.method == 'POST':
		edit_form = UserProfileForm(request.POST, instance=request.user)
		if edit_form.is_valid():
			edit_form.save()
			auth_login(request, request.user)
			messages.success(request, 'Профиль успешно изменён')
			return redirect('profile')
	else:
		edit_form = UserProfileForm(instance=request.user)
	return render(request, 'barter/edit_profile.html', context={'form':edit_form})

@login_required
@require_http_methods(['GET'])
def delete_account(request):
	# Удаление пользователя
	user = request.user
	logout(request)
	user.delete()
	return redirect('/')

@login_required
@require_http_methods(['GET'])
def ads_list(request):
	# Список всех объявлений.
	query = request.GET.get('q')  # Поисковый запрос
	category = request.GET.get('category')  # Фильтр по категории
	condition = request.GET.get('condition')  # Фильтр по состоянию

	ads = Ad.objects.all().order_by('-created_at')

	if query:
		# Поиск по заголовку и описанию
		ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
	if category:
		# Фильтрация по категории
		ads = ads.filter(category=category)
	if condition:
		# Фильтрация по состоянию
		ads = ads.filter(condition=condition)

	# Пагинация
	paginator = Paginator(ads, 10)  # Показывать по 10 объявлений на странице
	page_number = request.GET.get('page')  # Текущая страница
	page_obj = paginator.get_page(page_number)

	return render(request, 'barter/ads_list.html', {
		'page_obj': page_obj,
		'query': query,
		'category': category,
		'condition': condition,
		'CATEGORY_CHOICES':Ad.CATEGORY_CHOICES,
		'CONDITION_CHOICES':Ad.CONDITION_CHOICES
	})

@login_required
@require_http_methods(['GET'])
def show_ad(request, id: int):
	# Показывает объявление по id.
	if request.method == 'GET':
		ad = get_object_or_404(Ad, id=id)
		return render(request, 'barter/show_ad.html', context={'ad':ad})

@login_required
@require_http_methods(['GET', 'POST'])
def create_ad(request):
	# Создание объявления
	if request.method == 'POST':
		ad_form = AdForm(request.POST)
		if ad_form.is_valid():
			try:
				ad = ad_form.save(commit=False)
				ad.user = request.user
				ad.save()
				messages.success(request, 'Объявление успешно создано.')
				return redirect('show_ad', ad.id)
			except Exception as e:
				messages.error(request, 'Произошла ошибка при создании объявления. Попробуйте позже.')
	else:
		ad_form = AdForm()
	return render(request, 'barter/create_ad.html', context={'form':ad_form})

@login_required
@require_http_methods(['GET', 'POST'])
def edit_ad(request, id):
	# Изменение существующего объявления.
	ad = get_object_or_404(Ad, id=id)
	if ad.user != request.user:
		messages.error(request, "Вы не имеете права на изменения данного объявления")
		return redirect('ads_list')
	if request.method == 'POST':
		edit_ad_form = AdForm(request.POST, instance=ad)
		if edit_ad_form.is_valid():
			try:
				ad = edit_ad_form.save()
				messages.success(request, 'Объявление успешно изменено.')
				return redirect('show_ad', ad.id)
			except Exception as e:
				messages.error(request, 'Произошла при редактировании объявления.')
	else:
		edit_ad_form = AdForm(instance=ad)
	return render(request, 'barter/edit_ad.html', context={'form':edit_ad_form})

@login_required
@require_http_methods(['GET'])
def delete_ad(request, id):
	# Удаление объявления
	ad = get_object_or_404(Ad, id=id)
	if ad.user != request.user:
		message.error(request, "Вы не имеете права на изменения данного объявления")
		return redirect('ads_list')
	ad.delete()
	messages.success(request, 'Объявление успешно удалено.')
	return redirect('ads_list')

@login_required
@require_http_methods(['GET', 'POST'])
def create_exchange_proposal(request, ad_receiver_id):
	# Создание Предложения обмена.
	ad_receiver = get_object_or_404(Ad, id=ad_receiver_id)
	user_ads = Ad.objects.filter(user=request.user)
	if request.method == 'POST':
		proposal_form = ExchangeProposalForm(request.POST)
		if proposal_form.is_valid():
			try:
				ad_sender = proposal_form.cleaned_data['ad_sender']
				comment = proposal_form.cleaned_data['comment']

				ExchangeProposal.objects.create(
					ad_sender=ad_sender,
					ad_receiver=ad_receiver,
					comment=comment,
					status='W'
					)
				messages.success(request, 'Предложение обмена успешно создано.')
				return redirect('list_exchange_proposals')
			except Exception as e:
				messages.error(request, 'Произошла ошибка.')
	else:
		proposal_form = ExchangeProposalForm()
	return render(request, 'barter/create_exchange_proposal.html', context={
		'form':proposal_form,
		'ad_receiver':ad_receiver,
		'user_ads':user_ads
		})

@login_required
@require_http_methods(['GET'])
def list_exchange_proposals(request):
	# Просмотр Предложений обмена
	proposals = ExchangeProposal.objects.filter(Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user))

	# Фильтрация по отправителю
	sender_username = request.GET.get('sender_username')
	if sender_username:
		sender_ad = Ad.objects.filter(user__username=sender_username).first()
		if sender_ad:
			proposals = proposals.filter(ad_sender=sender_ad)

	# Фильтрация по получателю
	receiver_username = request.GET.get('receiver_username')
	if receiver_username:
		receiver_ad = Ad.objects.filter(user__username=receiver_username).first()
		if receiver_ad:
			proposals = proposals.filter(ad_receiver=receiver_ad)

	# Фильтрация по статусу
	status = request.GET.get('status')
	if status:
		proposals = proposals.filter(status=status)

	return render(request, 'barter/list_exchange_proposals.html', {'proposals': proposals})

@login_required
@require_http_methods(['GET', 'POST'])
def update_exchange_proposal(request, proposal_id):
	# Обновление статуса Предложения обмена
	proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

	if request.user not in [proposal.ad_sender.user, proposal.ad_receiver.user]:
		return redirect('profile')

	if request.method == 'POST':
		if proposal.ad_receiver.user == request.user:
			status = request.POST.get('status')
			if status in ['W', 'G', 'R']:
				try:
					proposal.status = status
					proposal.save()
					messages.success(request, 'Успешно изменён статус.')
					return redirect('list_exchange_proposals')
				except Exception as e:
					messages.error(request, 'Произошла ошибка при смене статуса.')
		else:
			messages.error(request, 'Менять статус может только получатель')
			return redirect('list_exchange_proposals')

	return render(request, 'barter/update_exchange_proposal.html', {'proposal': proposal})
