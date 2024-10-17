from django.db import models

from users.models import User


class MailAuthorization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    email_verified = models.BooleanField(default=False, verbose_name='Подтвержденный адрес электронной почты')

    class Meta:
        verbose_name = 'Авторизированная почта'
        verbose_name_plural = 'Авторизированные почты'

    def __str__(self):
        return f'Авторизация для {self.user}'


class Email(models.Model):
    authorization = models.ForeignKey(MailAuthorization, on_delete=models.CASCADE, related_name='emails',
                                      verbose_name='Авторизация', null=True)
    email = models.EmailField(verbose_name='Электронная почта')

    class Meta:
        verbose_name = 'Электронная почта'
        verbose_name_plural = 'Электронные почты'

    def __str__(self):
        return self.email


class Mails(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Айди")
    author = models.ForeignKey(MailAuthorization, on_delete=models.CASCADE, related_name='mails',
                               verbose_name='Автор')
    theme = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тема")
    date_send = models.DateField(verbose_name="Дата отправки")
    date_take = models.DateField(verbose_name="Дата получения", auto_now=True)
    description = models.TextField(blank=True, null=True, verbose_name="Содержание")
    files = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)

    class Meta:
        db_table = 'Mail'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.theme or "Без темы"


class File(models.Model):
    mail = models.ForeignKey(Mails, related_name='attachments', on_delete=models.CASCADE, verbose_name='Письмо')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', verbose_name='Файл')

    class Meta:
        verbose_name = 'Прикрепленный файл'
        verbose_name_plural = 'Прикрепленные файлы'

    def __str__(self):
        return self.file.name
