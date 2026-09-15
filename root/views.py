from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {
        'project_name': 'Docker Django Jinja Template',
        'engine': 'Jinja2',
    })
