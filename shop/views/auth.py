from django.shortcuts import render

def login_page(request):
    return render(request, 'auth/login.html')

def create_account(request):
    return render(request, 'auth/create_account.html')

def forgot_password(request):
    return render(request, 'auth/forgot_password.html')
