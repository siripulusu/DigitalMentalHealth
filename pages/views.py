from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    return render(request, 'pages/contact.html')

def resources_page(request):
    return render(request, 'pages/resources.html')

def helpline(request):
    return render(request, "pages/helpline.html")

