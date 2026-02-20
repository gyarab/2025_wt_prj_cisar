from django.shortcuts import render

def render_home(request):
    return render(request, 'app/home.html')

def render_about(request):
    return render(request, 'about.html')


