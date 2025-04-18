from django import forms
from .models import Ship, Group, AuctionListing
from django.contrib.auth.models import User

class ShipForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = ['owner']  # Only allow editing the 'stock' attribute

class ShipUpdateForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = ['nickname', 'harbor']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new nickname'}),
            'harbor': forms.Select(attrs={'class': 'form-control'})
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

class InviteUserForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=User.objects.none(), label="Select User")
    

    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users', User.objects.none())  # Get the users passed from the view
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = users  # Set the queryset for the dropdown


class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['buy_now_price', 'starting_bid', 'details', 'end_time']
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class BidForm(forms.Form):
    bid_amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)