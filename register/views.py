from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileUpdateForm, UserUpdateForm
from fishbanksapp.models import Ship
from django.contrib.auth import logout, authenticate, login



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            new_user.profile.balance = 20000
            new_user.save()
            Ship.objects.create(name='Starter Ship', fishing_capacity=1000, fishing_rate=500, description='starting vessel', owner=new_user, nickname='Starter Ship', cost=10000)
        return redirect("/")

    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {"form":form})


def logout_view(request):
    logout(request)
    return redirect('')

def settings_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('settings')
    else:
        # ✅ This is where the form pulls default values from
        u_form = UserUpdateForm(instance=request.user)
        u_form.initial['username'] = request.user.username
        u_form.initial['email'] = request.user.email
        p_form = ProfileUpdateForm(instance=request.user.profile)
        p_form.initial['bio'] = request.user.profile.bio

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'register/settings.html', context)
