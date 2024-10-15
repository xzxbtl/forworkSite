from django.shortcuts import render


def home(request):
    content = {
        'title': 'Home - Page',
    }
    return render(request, 'emailapp/home.html', content)
