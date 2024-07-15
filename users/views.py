from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from users.forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth

# Create your views here.

def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            print('not valid')
    else:
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'users/login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Vi uspeshno zaregistrirovalis!')
            return HttpResponseRedirect(reverse('users:login')) 
        else:
            print('not valid')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))



