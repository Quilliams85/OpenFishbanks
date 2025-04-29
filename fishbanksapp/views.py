from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Ship, FishSpecies, InGameTime, Invoice, Harbor, ManufacturerShip, Group, Invitation, Transaction, AuctionListing, TradeRequest
from django.db.models import Count
from django.contrib.auth.models import User
from .forms import ShipForm, ShipUpdateForm, GroupForm, InviteUserForm, AuctionListingForm, BidForm, TradeRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import plotly.express as px
import pandas as pd
from django.http import JsonResponse
import json
from datetime import datetime, timedelta
from .utils import send_invitation_email
import csv
from collections import defaultdict
from django.utils import timezone
from datetime import time

# Create your views here.


def get_game_time(request):
    t = InGameTime.objects.first()
    return JsonResponse({'time': t.formatTime(t.getTime())})


def home(request):
    harbors = Harbor.objects.all()
    return render(request, 'fishbanksapp/home.html', {'harbors':harbors})


def shop(request):
    now = timezone.localtime().time()  # This will be in your project's TIME_ZONE

    # Define quiet hours (23:00 to 09:00)
    start = time(23, 0)
    end = time(7, 0)

    if start <= now or now <= end:
        return render(request, 'fishbanksapp/shop_offline.html')
    else:
        listings = AuctionListing.objects.filter(status='pending').exclude(listing_owner=request.user)
        ships = ManufacturerShip.objects.all()

        bid_forms = {listing.id: BidForm() for listing in listings}

        return render(request, 'fishbanksapp/shop.html', {
            'ships': ships,
            'listings': listings,
            'bid_forms': bid_forms
        })

@login_required
def purchase_ship(request, ship_id):
    ship = get_object_or_404(ManufacturerShip, id=ship_id)
    user = request.user


    if (user.profile.balance >= ship.base_cost) and (ship.stock > 0):
        user.profile.balance -= ship.base_cost
        user.profile.save()
        ship.sellShip(user)
        ship.save()
        return render(request, 'fishbanksapp/successful_purchase.html', {'item': ship.name})
    else:
        return render(request, 'fishbanksapp/unsuccessful_purchase.html', {'item': ship.name})
    
def myprofile(request):
    return redirect('user_profile', username=request.user.username)
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
    groups = Group.objects.filter(members=user)
    ships = Ship.objects.filter(owner=user)
    context = {
        'profile_user': user,
        'profile': profile,
        'groups':groups,
        'ships':ships
    }
    return render(request, 'fishbanksapp/user_profile.html', context)

def leaderboard(request):
    users = User.objects.all()  # Fetch all users

    sorted_users = sorted(users, key=lambda user: user.profile.balance, reverse=True)
    user_groups = {}

    for user in sorted_users: # get groups for user and assign in dict
        groups = Group.objects.filter(members=user)
        if not groups:
            user_groups[user] = None
        else:
            for group in groups:      
                user_groups[user] = group

    context = {
        'users': sorted_users,
        'user_groups':user_groups
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

@login_required    
def invoice(request, invoice_id):
    user = request.user
    invoice = get_object_or_404(Invoice, id=invoice_id)
    profits = invoice.getProfit()
    if invoice.user != user:
        return None
    return render(request, 'fishbanksapp/invoice.html', {'invoice':invoice, 'profit':profits, 'num':invoice_id})

@login_required
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


@login_required
def invoice_list(request):
    user = request.user

    invoices = Invoice.objects.all().filter(user=user)
    invoices = list(invoices)[::-1]

    return render(request, 'fishbanksapp/invoice_list.html', {'invoices':invoices})

@login_required
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

@login_required
def user_inventory(request):
    user = request.user
    locations= {}
    for ship in Ship.objects.filter(owner=user):
        if ship.harbor not in locations:
            locations[ship.harbor] = [ship]
        else:
            locations[ship.harbor].append(ship)
    
    listings = AuctionListing.objects.filter(listing_owner=user, status='pending')
    ships = Ship.objects.filter(owner=user)
    return render(request, 'fishbanksapp/user_inventory.html', {'ships':ships, 'locations':locations, 'listings':listings})

@login_required
def user_transactions(request):
    user = request.user
    transactions = Transaction.objects.filter(reciever=user)
    transactions |= Transaction.objects.filter(sender=user)
    transactions = list(transactions)[::-1]
    return render(request, 'fishbanksapp/user_transactions.html', {'transactions':transactions})

@login_required
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

@login_required
def add_member(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.user == group.creator:  # Only the creator can add members
        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            group.members.add(user)
            return redirect('group_detail', group.id)
    return redirect('group_detail', group.id)

@login_required
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

@login_required
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

@login_required
def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.user == group.owner:
        group.delete()
    return redirect('groups')

@login_required
def create_listing(request, ship_id):
    ship = Ship.objects.get(id=ship_id)
    user = request.user
    if request.method == 'POST':
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.ship = ship
            listing.listing_owner = user
            ship.owner = None
            ship.save()
            listing.save()
            return redirect('/shop')
    else:
        form = AuctionListingForm()
    return render(request, 'fishbanksapp/create_listing.html', {'form': form, 'ship':ship})

@login_required
def buy_now(request, auction_id):
    listing = AuctionListing.objects.get(id=auction_id)
    if (request.user.profile.balance > listing.buy_now_price) and listing.status == 'pending':
        listing.current_bidder = request.user
        listing.current_bid = listing.buy_now_price
        listing.save()
        listing.sellShip()
    return redirect('inventory')

@login_required
def place_bid(request, auction_id):
    auction = get_object_or_404(AuctionListing, id=auction_id)
    
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data["bid_amount"]
            if (bid_amount >= auction.current_bid + 500.0) and request.user.profile.balance > bid_amount:  # Ensure it's a higher bid and 500 more
                auction.current_bid = bid_amount
                auction.current_bidder = request.user
                auction.save()
                messages.success(request, "Your bid was placed successfully!")
            else:
                messages.error(request, "Your bid must be higher than the current bid or insufficient funds.")

    return redirect("shop")  # Redirect to auction detail page

@login_required
def harbors(request):
    harbors = Harbor.objects.all()
    return render(request, 'fishbanksapp/harbors.html', {'harbors': harbors})

@login_required
def harbor_detail(request, harbor_id):
    harbor = Harbor.objects.get(id=harbor_id)
    ships = Ship.objects.filter(harbor=harbor)
    species = FishSpecies.objects.filter(harbor=harbor)
    current_population = len(ships)
    return render(request, 'fishbanksapp/harbor_detail.html', {'harbor': harbor, 'current_population': current_population, 'species':species})

@login_required
def fish_market(request):
    species = FishSpecies.objects.all()
    return render(request, 'fishbanksapp/fish_market.html', {'species': species})


@login_required
def create_trade_request(request):
    recipient_id = request.GET.get('recipient')
    recipient = get_object_or_404(User, id=recipient_id) if recipient_id else None
    if request.method == 'POST':
        form = TradeRequestForm(request.POST, user=request.user, recipient=recipient)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.sender = request.user
            trade.recipient = recipient
            trade.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = TradeRequestForm(user=request.user, recipient=recipient)
    return render(request, 'fishbanksapp/create_trade.html', {'form': form, 'recipient': recipient})

@login_required
def view_trades(request):
    users = User.objects.exclude(id=request.user.id)
    incoming_pending = request.user.received_trades.filter(status='pending')
    outgoing_pending = request.user.sent_trades.filter(status='pending')
    incoming_past = request.user.received_trades.exclude(status='pending')
    outgoing_past = request.user.sent_trades.exclude(status='pending')
    return render(request, 'fishbanksapp/view_trades.html', {'incoming_pending': incoming_pending, 'outgoing_pending': outgoing_pending, 'incoming_past':incoming_past, 'outgoing_past':outgoing_past, 'users':users})

@login_required
def respond_to_trade(request, trade_id, response):
    trade = get_object_or_404(TradeRequest, id=trade_id, recipient=request.user)
    if trade.status != 'pending':
        messages.error(request, 'Trade already responded to.')
        return redirect('view_trades')

    if response == 'accept':
        # Transfer money
        if trade.sender.profile.balance >= trade.money_requested and trade.recipient.profile.balance >= trade.money_offered:
            date = InGameTime.objects.first().getFormattedTime()
            Transaction.objects.create(sender=trade.sender, reciever=trade.recipient,
            transaction_type=Transaction.TransactionType.STORE_TO_PLAYER,
            content_type=None,
            object_id=None,
            date=date)
            trade.sender.profile.balance += float(trade.money_requested)
            trade.recipient.profile.balance += float(trade.money_offered)
            trade.sender.profile.balance -= float(trade.money_offered)
            trade.recipient.profile.balance -= float(trade.money_requested)

            trade.sender.profile.save()
            trade.recipient.profile.save()

            # Transfer ships
            for ship in trade.offered_ships.all():
                ship.owner = trade.recipient
                ship.save()
            for ship in trade.requested_ships.all():
                ship.owner = trade.sender
                ship.save()

            trade.status = 'accepted'
        else:
            messages.error(request, 'Insufficient balance to complete the trade.')
            return redirect('view_trades')
    else:
        trade.status = 'rejected'
    trade.save()
    messages.success(request, f'Trade {trade.status}.')
    return redirect('view_trades')


def export_fish_data_csv(request):
    # Step 1: Gather all history entries and round timestamps
    species_names = [species.name for species in FishSpecies.objects.all()]
    data_by_time = defaultdict(dict)

    for species in FishSpecies.objects.all():
        for his in species.history.all():
            # Round to nearest second (or minute, if you prefer)
            rounded_time = his.history_date.replace(microsecond=0)
            data_by_time[rounded_time][species.name] = his.population

    # Step 2: Sort timestamps
    sorted_timestamps = sorted(data_by_time.keys())

    # Step 3: Prepare CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fish_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['timestamp'] + species_names)

    # Step 4: Build and write rows
    last_known_values = {name: '' for name in species_names}

    for timestamp in sorted_timestamps:
        # Update last known values if available
        for name in species_names:
            if name in data_by_time[timestamp]:
                last_known_values[name] = data_by_time[timestamp][name]

        # Write row with the most recent known values
        row = [timestamp] + [last_known_values[name] for name in species_names]
        writer.writerow(row)

    return response


def api_leaderboard(request):
    users = User.objects.all()  # Fetch all users
    sorted_users = sorted(users, key=lambda user: user.profile.balance, reverse=True)
    usernames = {}
    for user in sorted_users:
        usernames[user.username] = user.profile.balance

    return JsonResponse(usernames)

def net_worth_leaderboard(request):
    users = User.objects.all()
    user_groups = {}

    net_worths = {}
    for user in users:
        balance = user.profile.balance
        for ship in Ship.objects.filter(owner=user):
            balance += ship.cost
        net_worths[user.username] = balance

    sorted_users = sorted(users, key=lambda user: net_worths[user.username], reverse=True)

    for user in sorted_users:  # get groups for user and assign in dict
        groups = Group.objects.filter(members=user)
        if not groups:
            user_groups[user] = None
        else:
            for group in groups:      
                user_groups[user] = group

    context = {
        'users': sorted_users,
        'user_groups': user_groups,
        'net_worths': net_worths,
    }
    return render(request, 'fishbanksapp/net_leaderboard.html', context)
