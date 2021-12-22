from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import SignUpForm

def main(request):
    if request.user.is_authenticated:
        return redirect(reverse('leases:index'))
    if request.method == 'GET':
        return render(request, 'users/main.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('leases:index'))
        else:
            return render(request, 'users/main.html')

def signup(request):
    if request.method == 'GET':
        form = SignUpForm()

        return render(request, 'users/signup.html', {'form': form})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('leases:index'))

        return render(request, 'users/main.html')

def logout(request):
    auth.logout(request)
    return render(request,'users/main.html')
