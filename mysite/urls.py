"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from barter import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), # Главная страница
    path('accounts/signup/', views.signup, name='signup'), # Страница регистрации
    path('accounts/login/', views.login, name='login'), # Страница авторизации
    path('account/logout/', views.logout_views, name='logout'), # Логаут с редиректом на главную страницу
    path('account/profile/', views.profile, name='profile'), # Страница профиля
    path('account/edit/', views.edit_profile, name='edit_profile'), # Страница редактирования профиля
    path('account/delete/', views.delete_account, name='delete_account'), # Удаление пользователя с редиректом на главную страницу
    path('ads/list/', views.ads_list, name='ads_list'), # Страница со списком Объявлений
    path('ads/<int:id>/', views.show_ad, name='show_ad'), # Страница просмотра Объявления по его id
    path('ads/create/', views.create_ad, name='create_ad'), # Страница создания Объявления
    path('ads/<int:id>/edit', views.edit_ad, name='edit_ad'), # Страница редактирования Объявления
    path('ads/<int:id>/delete', views.delete_ad, name='delete_ad'), # Удаление Объявления с редиректом на ads/list 
    path('exchange/create/<int:ad_receiver_id>/', views.create_exchange_proposal, name='create_exchange_proposal'), # Страница создания Предложения обмена
    path('exchange/list/', views.list_exchange_proposals, name='list_exchange_proposals'), # Страница со всеми Предложениями обмена пользователя
    path('exchange/update/<int:proposal_id>/', views.update_exchange_proposal, name='update_exchange_proposal'), # Страница редактирования Предложения обмена
]