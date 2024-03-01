from django import forms
from django.contrib.auth.models import User
from .models import Booking, Room
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserSignupForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        # Optionally, remove the help text for the username field
        self.fields['username'].help_text = ''

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # Use the new field names here
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
    
class BookingForm(forms.ModelForm):
    guest_name = forms.CharField(label='Guest Name', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Guest Name'}))
    checkin_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Check-in Date', 'format': 'd/m/Y'}))
    checkout_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Check-out Date', 'format': 'd/m/Y'}))
    room = forms.ModelChoiceField(queryset=Room.objects.all(), label='Room', empty_label="Select Room")

    class Meta:
        model = Booking
        fields = ['guest_name', 'checkin_date', 'checkout_date', 'room']

    def clean(self):
        cleaned_data = super().clean()
        checkin_date = cleaned_data.get('checkin_date')
        checkout_date = cleaned_data.get('checkout_date')
        room = cleaned_data.get('room')

        if checkin_date and checkout_date and room:
            if checkin_date > checkout_date:
                raise ValidationError("Checkout date must be after checkin date")

            duration = (checkout_date - checkin_date).days
            calculated_amount = room.price * duration

            # Since the amount is automatically calculated in the model, 
            # we don't need to set it here.
            # cleaned_data['amount'] = calculated_amount

        return cleaned_data

class PaymentForm(forms.Form):
    slip = forms.FileField(label='Upload Slip')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'image', 'beds', 'baths', 'size', 'rating', 'reviews_count', 'price']