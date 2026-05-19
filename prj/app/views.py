from django.shortcuts import render

def render_home(request):
    return render(request, 'app/home.html')

def render_about(request):
    return render(request, 'app/about.html')

def api_playground(request):
    return render(request, "api_playground.html")
