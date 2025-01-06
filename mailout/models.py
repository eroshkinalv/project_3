from django.db import models

from users.models import User


class Clients(models.Model):

    email = models.CharField(max_length=150, unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=150, verbose_name='Ф.И.О.')
    notes = models.TextField(null=True, blank=True, verbose_name='Комментарий')

    owner = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        ordering = ['email']


class Message(models.Model):

    subject = models.CharField(max_length=250, verbose_name='Тема')
    message = models.TextField(null=True, blank=True, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания сообщения')

    owner = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['created_at']


class Mailout(models.Model):

    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name='Рассылка создана', null=True, blank=True,)    #рассылка была создана, но еще ни разу не была отправлена
    sent_at = models.DateTimeField(verbose_name='Рассылка завершена', null=True, blank=True,)   #время окончания отправки рассылки прошло
    is_active = models.BooleanField(default=False, verbose_name='Рассылка запущена', null=True, blank=True,)   #рассылка активна и была отправлена хотя бы один раз

    STATUS_CHOICES = (('Создана', 'Создана'), ('Завершена', 'Завершена'), ('Запущена', 'Запущена'))
    status = models.CharField(max_length=250, verbose_name='Статус рассылки', choices=STATUS_CHOICES)

    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Clients, related_name="mailout")

    owner = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['message', 'sent_at', 'status']


class Attempt(models.Model):

    emailed_at = models.DateTimeField(auto_now_add=True, verbose_name='Попытка рассылки')

    STATUS_CHOICES = (('Успешно', 'Успешно'), ('Не успешно', 'Не успешно'))
    status = models.CharField(max_length=250, verbose_name='Статус рассылки', choices=STATUS_CHOICES)

    server_message = models.TextField(null=True, blank=True, verbose_name='Ответ почтового сервера')

    mailout = models.ForeignKey(Mailout, on_delete=models.CASCADE)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
        ordering = ['emailed_at', 'status']


class Home(models.Model):

    total_mailout = models.IntegerField(default=0, verbose_name='Количество всех рассылок')
    total_active = models.IntegerField(default=0, verbose_name='Количество активных рассылок')
    total_users = models.IntegerField(default=0, verbose_name='Количество уникальных получателей')

    def __str__(self):
        return self.total_mailout

    class Meta:
        verbose_name = 'статистика'
        verbose_name_plural = 'статистика'
        ordering = ['total_mailout', 'total_active', 'total_users']
