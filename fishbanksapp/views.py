from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import ToDoList, Item, Ship
from django.contrib.auth.models import User
from .forms import ShipForm

# Create your views here.

def home(request):
    return render(request, 'fishbanksapp/home.html', {"name":"test"})


def index(request, id):
    ls = ToDoList.objects.get(id=id)
    item = ls.item_set.get(id=1)
    return render(request, 'fishbanksapp/base.html', {"name":ls.name})

def shop(request):
    ships = []
    for i in Ship.objects.all():
        if i.stock > 0:
            ships.append(i)
    return render(request, 'fishbanksapp/shop.html', {'ships': ships})

def purchase_ship(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)
    user = request.user

    if user.profile.balance >= ship.cost:
        user.profile.balance -= ship.cost
        if str(ship.id) not in user.profile.ships_list:
            user.profile.ships_list[str(ship.id)] = 1
        else:
            user.profile.ships_list[str(ship.id)] += 1
        ship.stock -= 1
        user.profile.save()
        ship.save()
        return render(request, 'fishbanksapp/successful_purchase.html', {'item': ship.name})
    else:
        return render(request, 'fishbanksapp/unsuccessful_purchase.html', {'item': ship.name})
    
def myprofile(request):
    user = request.user
        
    balance = user.profile.balance

    # Get the ships and their quantities
    ships_and_quantities = []
    for ship_id, quantity in user.profile.ships_list.items():
        ship = Ship.objects.get(id=int(ship_id))  # Fetch the Ship object
        ships_and_quantities.append({
            'ship': ship,
            'quantity': quantity,
        })

    context = {
        'profile_user': user,
        'balance': balance,
        'ships_and_quantities': ships_and_quantities,
    }
    return render(request, 'fishbanksapp/profile.html', context)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile  # Access the related profile
    is_owner = (request.user == user)  # Check if the logged-in user is the profile owner
    if is_owner :
        return redirect('/myprofile/')
    context = {
        'profile_user': user,
        'profile': profile,
        'is_owner': is_owner,
    }
    return render(request, 'fishbanksapp/user_profile.html', context)

def leaderboard(request):
    users = User.objects.all()  # Fetch all users
    ordered_users = {}
    for i in users:
        ordered_users[str(i.username)] = i.profile.balance

    ordered_users = dict(sorted(ordered_users.items(), key=lambda item: item[1], reverse=True))
    context = {
        'users': users,
        'ordered_users': ordered_users
    }
    return render(request, 'fishbanksapp/leaderboard.html', context)

def config(request):
    ships = Ship.objects.all()
    if request.method == 'POST':
        # Handle form submissions
        for ship in ships:
            form = ShipForm(request.POST, prefix=str(ship.id), instance=ship)
            if form.is_valid():
                form.save()
        return redirect('shop')  # Redirect to refresh the page
    else:
        # Display forms for each ship
        forms = [ShipForm(prefix=str(ship.id), instance=ship) for ship in ships]
        # Zip ships and forms together
        ships_and_forms = zip(ships, forms)

    if request.user.is_superuser:
        return render(request, 'fishbanksapp/config.html', {'ships_and_forms': ships_and_forms})
    else:
        return HttpResponse('NO ACCESS')