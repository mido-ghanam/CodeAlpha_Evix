from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render

def login(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is None:
      messages.error(request, "Invalid username or password")
      return redirect('login')
  return render(request, 'login.html')

def registration(request):
  return render(request, 'registration.html')

