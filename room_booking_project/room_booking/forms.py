from django import forms
from django.contrib.auth.models import User
from .models import Booking, Room

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserSignupForm(forms.ModelForm):
    name = forms.CharField(label='Name')
    surname = forms.CharField(label='Surname')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'surname']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        if commit:
            user.save()
        return user
    
class BookingForm(forms.ModelForm):
    room = forms.ModelChoiceField(queryset=Room.objects.all(), label='Room')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Check-in Date')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Check-out Date')

    class Meta:
        model = Booking
        fields = ['room', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()

        # Example availability check: Adapt this for your exact logic
        if 'start_date' in cleaned_data and 'end_date' in cleaned_data and 'room' in cleaned_data:
            room = cleaned_data['room']
            start_date = cleaned_data['start_date']
            end_date = cleaned_data['end_date']

            if Booking.objects.filter(room=room).filter(
                start_date__lte=end_date,  # Start date falls within an existing booking 
                end_date__gte=start_date   # End date falls within an existing booking  
            ).exists():
                raise forms.ValidationError("Room is not available during selected dates")

class PaymentForm(forms.Form):
    slip = forms.FileField(label='Upload Payment Slip') 