from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Ship, FishSpecies, InGameTime, Invoice, Harbor, ManufacturerShip, Group, Invitation
from django.db.models import Count
from django.contrib.auth.models import User
from .forms import ShipForm, ShipUpdateForm, GroupForm, InviteUserForm
from django.contrib.auth.decorators import login_required
import plotly.express as px
import pandas as pd
from django.http import JsonResponse
import json
from datetime import datetime, timedelta
from .utils import send_invitation_email


# Create your views here.


def get_game_time(request):
    t = InGameTime.objects.first()
    return JsonResponse({'time': t.formatTime(t.getTime())})


def home(request):
    harbors = Harbor.objects.all()
    return render(request, 'fishbanksapp/home.html', {'harbors':harbors})


def shop(request):
    ships = ManufacturerShip.objects.all()
    return render(request, 'fishbanksapp/shop.html', {'ships': ships})

def purchase_ship(request, ship_id):
    ship = get_object_or_404(ManufacturerShip, id=ship_id)
    user = request.user

    if user.profile.balance >= ship.base_cost:
        user.profile.balance -= ship.base_cost
        user.profile.save()
        ship.sellShip(user)
        ship.save()
        return render(request, 'fishbanksapp/successful_purchase.html', {'item': ship.name})
    else:
        return render(request, 'fishbanksapp/unsuccessful_purchase.html', {'item': ship.name})
    
def myprofile(request):
    user = request.user        
    balance = user.profile.balance
    context = {
        'profile_user': user,
        'balance': balance,
    }
    return render(request, 'fishbanksapp/profile.html', context)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    is_owner = (request.user == user) 
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
    groups = Group.objects.all()
    ordered_users = {}
    for i in users:
        ordered_users[str(i.username)] = i.profile.balance

    ordered_users = dict(sorted(ordered_users.items(), key=lambda item: item[1], reverse=True))
    context = {
        'users': users,
        'ordered_users': ordered_users,
        'groups':groups
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
        forms = [ShipForm(prefix=str(ship.id), instance=ship) for ship in ships]
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

def modify(request, ship_id):
    user = request.user
    ship = Ship.objects.get(id=ship_id)
    harbors = Harbor.objects.all()
    if ship.owner != user:
        return None


    if request.method == "POST":
        form = ShipUpdateForm(request.POST, instance=ship)
        if form.is_valid():
            form.save()
            return redirect('/inventory')
    else:
        form = ShipUpdateForm(instance=ship)
    harbors_json = {harbor.id: {"name": harbor.name, "fee": harbor.storage_fee, "description": harbor.description} for harbor in harbors}

    context = {
        'ship': ship,
        'harbors': harbors,
        "form": form,
        "harbors_json": json.dumps(harbors_json)
    }
    return render(request, 'fishbanksapp/modify.html', context)

def invoice_list(request):
    user = request.user

    invoices = Invoice.objects.all().filter(user=user)
    invoices = list(invoices)[::-1]

    return render(request, 'fishbanksapp/invoice_list.html', {'invoices':invoices})

def user_finances(request):
    user = request.user
        
    balance = user.profile.balance
    user_history = user.profile.history.all()
    dates = [record.history_date for record in user_history]
    balances = [record.balance for record in user_history]


    data = pd.DataFrame({
        'Date': dates[0:1000], 
        'Balance': balances[0:1000],
    })
    data['Date'] = pd.to_datetime(data['Date'])

    fig = px.line(data, x='Date', y='Balance')
    fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Balance($)",
    xaxis=dict(tickangle=-45, tickfont=dict(size=12)),
    yaxis=dict(tickfont=dict(size=12)),
    legend=dict(title='Legend', x=0.8, y=1.1))
    chart_html = fig.to_html(full_html=False)

    data['Date'] = pd.to_datetime(data['Date'])
    one_month_ago = pd.Timestamp.today() - pd.DateOffset(days=1)
    one_month_ago = one_month_ago.tz_localize('UTC')
    if (user.date_joined.timestamp() - one_month_ago.timestamp()) < 0: #If one month ago is before user creation, set default=0
        closest_balance = data.loc[data['Date'] <= one_month_ago].sort_values(by='Date', ascending=False).iloc[0]
        balance_increase = user.profile.balance - closest_balance['Balance']
    else:
        balance_increase = 0

    context = {
        'profile_user': user,
        'balance': balance,
        'chart_html': chart_html,
        'balance_increase': balance_increase,
    }
    return render(request, 'fishbanksapp/user_finances.html', context)

def about(request):
    return render(request, 'fishbanksapp/about.html')

def user_inventory(request):
    user = request.user
    locations= {}
    for ship in Ship.objects.filter(owner=user):
        if ship.harbor not in locations:
            locations[ship.harbor] = [ship]
        else:
            locations[ship.harbor].append(ship)
        
    ships = Ship.objects.filter(owner=user)
    return render(request, 'fishbanksapp/user_inventory.html', {'ships':ships, 'locations':locations})

def user_transactions(request):
    return render(request, 'fishbanksapp/user_transactions.html')


def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            group.members.add(request.user)  # Add the creator as a member
            return redirect('/groups')
    else:
        form = GroupForm()
    return render(request, 'fishbanksapp/create_group.html', {'form': form})

def add_member(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.user == group.creator:  # Only the creator can add members
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            group.members.add(user)
            return redirect('group_detail', group.id)
    return redirect('group_detail', group.id)

def group_detail(request, group_id):

    group = get_object_or_404(Group, id=group_id)
    users = User.objects.exclude(id__in=group.members.values_list('id', flat=True))  # Exclude existing members

    if request.method == 'POST' and 'send_invite' in request.POST:
        form = InviteUserForm(request.POST, users=users)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            # Create an invitation
            invitation = Invitation.objects.create(
                sender=request.user,
                recipient=recipient,
                group=group,
                status='pending'
            )
            return redirect('group_detail', group.id)
    else:
        form = InviteUserForm(users=users)

    # Get pending invitations for this group
    pending_invitations = Invitation.objects.filter(group=group, status='pending')

    return render(request, 'fishbanksapp/group_detail.html', {
        'group': group,
        'form': form,
        'pending_invitations': pending_invitations,
    })

def user_groups(request):
    user = request.user
    groups = Group.objects.filter(members=user)
    invitations = Invitation.objects.filter(recipient=user, status='pending')
    return render(request, 'fishbanksapp/user_groups.html',{'groups': groups, 'invitations':invitations})


@login_required
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id, recipient=request.user)
    if invitation.status == 'pending':
        invitation.status = 'accepted'
        invitation.save()
        invitation.group.members.add(request.user)
    return redirect('group_detail', invitation.group.id)

@login_required
def decline_invitation(request, invitation_id):
    invitation = get_object_or_404(Invitation, id=invitation_id, recipient=request.user)
    if invitation.status == 'pending':
        invitation.status = 'declined'
        invitation.save()
    return redirect('groups')

def leave_group(request, group_id):
    user = request.user
    group = Group.objects.get(id=group_id)
    group.members.remove(user)
    return redirect('groups')

def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.delete()
    return redirect('groups')