from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import ToDoList, Item, Ship
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    return render(request, 'fishbanksapp/home.html', {"name":"test"})


def index(request, id):
    ls = ToDoList.objects.get(id=id)
    item = ls.item_set.get(id=1)
    return render(request, 'fishbanksapp/base.html', {"name":ls.name})

def shop(request):
    pass

def buy_ship(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    user = request.user

    if user.profile.balance >= ship.cost:
        user.profile.balance -= ship.cost
        ship.owner = user
        ship.save()
        user.profile.save()
        return render(request, 'success.html', {'message': 'Ship purchased successfully!'})
    else:
        return render(request, 'error.html', {'message': 'Insufficient funds!'})
    
def profile(request):
    return render(request, 'fishbanksapp/profile.html')

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'profile_user': user,
    }
    return render(request, 'fishbanksapp/user_profile.html', context)

def leaderboard(request):
    users = User.objects.all()  # Fetch all users
    context = {
        'users': users,
    }
    return render(request, 'fishbanksapp/leaderboard.html', context)