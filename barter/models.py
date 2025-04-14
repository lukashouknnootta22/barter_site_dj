from django.db import models
from django.contrib.auth.models import User

# Модель объявления.
class Ad(models.Model):

	CONDITION_CHOICES = (
		('N', 'Новый'),
		('U', 'Б/у')
	)

	CATEGORY_CHOICES = (
		('E', 'Электроника'),
		('C', 'Вещи')
		)
	
	user = models.ForeignKey(User, on_delete=models.CASCADE) #user_id 
	title = models.CharField(max_length=200) # Заголовок объявления
	description = models.TextField() # Описание товара
	image_url = models.URLField(blank=True, null=True) # Опцианально - изображения товара
	category = models.CharField(max_length=200, choices=CATEGORY_CHOICES) # Категория товара
	condition = models.CharField(max_length=10, choices=CONDITION_CHOICES) # Состояние товара
	created_at = models.DateTimeField(auto_now_add=True) # Авто-фиксация времени публикации

	def __str__(self):
		return self.title

# Модель Предложения обмена.
class ExchangeProposal(models.Model):

	STATUS_CHOICES = (
	('W', 'Ожидает',),
	('G', 'Принята',),
	('R', 'Отклонена'),
	)

	ad_sender = models.ForeignKey(Ad, related_name='sender_id', on_delete=models.CASCADE) # user Отправитель
	ad_receiver = models.ForeignKey(Ad, related_name='receiver_id', on_delete=models.CASCADE) # user Получатель
	comment = models.CharField(max_length=200, blank=True, null=True) # Опцианально - сообщение
	status = models.CharField(max_length=20, choices=STATUS_CHOICES) # Статус предложения
	created_at = models.DateTimeField(auto_now_add=True) # Авто-фиксация времени публикации

# Модель Новостей.
class News(models.Model):
	title = models.CharField(max_length=200)  # Заголовок новости
	content = models.TextField()  # Текст новости
	created_at = models.DateTimeField(auto_now_add=True)  # Авто-фиксация времени публикации

	def __str__(self):
		return self.title