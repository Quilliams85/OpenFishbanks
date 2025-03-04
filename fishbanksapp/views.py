from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import ToDoList, Ship, FishSpecies, InGameTime, Invoice
from django.contrib.auth.models import User
from .forms import ShipForm
import plotly.express as px
import pandas as pd
from django.http import JsonResponse


# Create your views here.


def get_game_time(request):
    t = InGameTime.objects.first()
    return JsonResponse({'time': t.formatTime(t.getTime())})


def home(request):
    return render(request, 'fishbanksapp/home.html')


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
    invoices = Invoice.objects.filter(user=user)
        
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
        'invoices': invoices
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
    fish_history = FishSpecies.history.all()

    salmon = FishSpecies.objects.get(id=1)
    salmon_history = salmon.history.all()
    dates = [record.history_date for record in salmon_history]
    populations = [record.population for record in salmon_history]


    data = pd.DataFrame({
        'Date': dates[0:1000], 
        'Population': populations[0:1000],
    })

    # Create the chart
    fig = px.line(data, x='Date', y='Population', title=f"Population Change Over Time for {salmon.name}")
    fig.update_layout(
    title=dict(text="Population Change Over Time", x=0.5, font=dict(size=20, color='darkblue')),
    xaxis_title="Date",
    yaxis_title="Population",
    xaxis=dict(tickangle=-45, tickfont=dict(size=12)),
    yaxis=dict(tickfont=dict(size=12)),
    legend=dict(title='Legend', x=0.8, y=1.1))
    # Convert the chart to HTML
    chart_html = fig.to_html(full_html=False)

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
        return render(request, 'fishbanksapp/config.html', {'ships_and_forms': ships_and_forms, 'history':fish_history, 'chart_html': chart_html})
    else:
        return HttpResponse('NO ACCESS')
    
def invoice(request, invoice_id):
    user = request.user
    invoice = get_object_or_404(Invoice, id=invoice_id)
    profits = invoice.getProfit()
    if invoice.user != user:
        return None
    return render(request, 'fishbanksapp/invoice.html', {'invoice':invoice, 'profit':profits, 'num':invoice_id})