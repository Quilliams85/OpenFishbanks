from django import forms
from .models import Ship

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