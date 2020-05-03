from django.shortcuts import render


def home(request):
    return render(request=request, template_name='app/index.html', status=200)
