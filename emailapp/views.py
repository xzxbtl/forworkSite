from smtplib import SMTP, SMTPAuthenticationError
from django.shortcuts import render
from django.urls import reverse

from users.models import User
from email.mime.text import MIMEText
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import MailRegistrationForm
from .models import MailAuthorization, Email


def home(request):
    try:
        mail_auth_user = MailAuthorization.objects.get(user=request.user)
        emails = mail_auth_user.emails.all()
    except Exception as err:
        print(f"Ошибка - {err}")
        emails = []

    options = []

    for mail in emails:
        options.append(f'<option value="{mail.id}">{mail.email}</option>')

    if not options:
        options.append('<option value="default" selected>yourmail@example.com</option>')

    content = {
        'title': 'Home - Page',
        'email_options': 'n'.join(options),
    }
    return render(request, 'emailapp/home.html', content)


def auntificate_mail(email, password):
    try:
        if email.endswith("@gmail.com"):
            host = SMTP('smtp.gmail.com', 587)
        elif email.endswith("@mail.ru"):
            host = SMTP('smtp.mail.ru', 587)
        elif email.endswith("@yandex.ru"):
            host = SMTP('smtp.yandex.ru', 587)
        else:
            print("Неподдерживаемый домен электронной почты.")
            return False

        host.starttls()
        host.login(email, password)
        host.quit()
        return True

    except SMTPAuthenticationError:
        print("Ошибка аутентификации: неверный адрес электронной почты или пароль.")
        return False

    except Exception as err:
        print(f"Ошибка - {err}")
        return False


@login_required
def add_mail(request):
    if request.method == 'POST':
        form = MailRegistrationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if auntificate_mail(email, password):
                mail_auth, created = MailAuthorization.objects.get_or_create(user=request.user)
                if not Email.objects.filter(authorization=mail_auth, email=email).exists():
                    Email.objects.create(authorization=mail_auth, email=email)
                    messages.success(request, 'Почта добавлена успешно!')
                    return HttpResponseRedirect(reverse('emailapp:home'))
                else:
                    messages.info(request, 'Этот адрес электронной почты уже добавлен.')
                    return HttpResponseRedirect(reverse('emailapp:mailadd'))
            else:
                messages.error(request, 'Неверный адрес электронной почты или пароль.')
                return HttpResponseRedirect(reverse('emailapp:mailadd'))

    else:
        form = MailRegistrationForm()

    context = {
        'title': 'Email Authorization',
        'form': form
    }

    return render(request, 'emailapp/emailadd.html', context)

