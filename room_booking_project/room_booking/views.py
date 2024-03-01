from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import PaymentSlip, Room, Booking
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import BookingForm, PaymentForm, UserLoginForm, UserSignupForm
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import UserForm
from .forms import RoomForm
from django.utils.timezone import datetime
from django.db.models import Sum, Count

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserSignupForm()
    return render(request, 'room_booking/signup.html', {'form': form})

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Redirect based on user type
                if user.is_staff:  # Assuming admins have is_staff flag set 
                    return redirect('admin_dashboard')  
                else:
                    return redirect('/')  
            else:
                pass
    return render(request, 'room_booking/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()  # Save booking without setting amount (it will be calculated automatically)
            return redirect('payment_page', room_id=room_id)
    else:
        form = BookingForm()
    return render(request, 'room_booking/book_room.html', {'room': room, 'form': form})

def booking_success(request):
    return render(request, 'room_booking/booking_success.html')

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_booking/room_list.html', {'rooms': rooms})

def room_details(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'room_booking/room_details.html', {'room': room})

def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    bookings = Booking.objects.filter(user=user)
    return render(request, 'room_booking/user_profile.html', {'user': user, 'bookings': bookings})

@login_required
def payment_page(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['slip']
            payment_amount = room.price

            # Retrieve the associated booking for the user and room
            booking = Booking.objects.filter(user=request.user, room=room).first()
            if booking:
                guest_name = booking.guest_name
                PaymentSlip.objects.create(
                    user=request.user,
                    room=room,
                    slip=uploaded_file,
                    verified=False,
                    booking=booking,  # Associate the PaymentSlip with the booking
                    guest_name=guest_name  # Include the guest name
                )
                countdown_end = timezone.now() + timedelta(minutes=10)
                request.session['countdown_end'] = countdown_end.isoformat()
                return render(request, 'room_booking/waiting_verification.html', {'room_id': room_id})
            else:
                messages.error(request, 'Booking not found.')
        else:
            messages.error(request, 'There was an error with your submission. Please check your data and try again.')
    else:
        form = PaymentForm()

    
    payment_amount = room.price
    context = {
        'form': form,
        'payment_amount': payment_amount,
        'bank_details': 'ABC Bank\nAccount Number: 123456789',
        'room_id': room_id,
    }
    return render(request, 'room_booking/payment_page.html', context)

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'room_booking/booking_history.html', {'bookings': bookings})

@user_passes_test(lambda u: u.is_superuser)
def admin_payment_slips(request):
    payment_slips = PaymentSlip.objects.filter(verified=False)
    return render(request, 'room_booking/admin_payment_slips.html', {'payment_slips': payment_slips})

def verify_payment_slip(request, slip_id):
    payment_slip = get_object_or_404(PaymentSlip, id=slip_id)
    payment_slip.verified = True
    payment_slip.save()
    messages.success(request, 'Payment slip verified successfully.')
    return redirect('admin_dashboard')

def check_payment_status(request, room_id):
    payment_slip = PaymentSlip.objects.filter(room_id=room_id, user=request.user).first()
    
    if payment_slip:
        return JsonResponse({'is_verified': payment_slip.verified})
    else:
        return JsonResponse({'error': 'Payment slip not found'}, status=404)

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    payment_slips = PaymentSlip.objects.all()  # Retrieve all payment slips
    return render(request, 'room_booking/admin_dashboard.html', {'payment_slips': payment_slips})

@user_passes_test(lambda u: u.is_staff) 
def admin_statistics(request):
    return render(request, 'room_booking/admin_statistics.html')

@user_passes_test(lambda u: u.is_staff) 
def admin_profile(request):
    users = User.objects.all()
    return render(request, 'room_booking/admin_profile.html', {'users': users})

@user_passes_test(lambda u: u.is_staff) 
def admin_management(request):
    rooms = Room.objects.all()
    return render(request, 'room_booking/admin_management.html', {'rooms': rooms})

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_profile')
    else:
        form = UserForm()
    return render(request, 'room_booking/add_user.html', {'form': form})

def view_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'room_booking/view_user.html', {'user': user})

def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_profile')
    else:
        form = UserForm(instance=user)
    return render(request, 'room_booking/edit_user.html', {'form': form})

def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('admin_profile')

def view_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'room_booking/view_room.html', {'room': room})

def edit_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('admin_management')
    else:
        form = RoomForm(instance=room)
    return render(request, 'room_booking/edit_room.html', {'form': form})

def delete_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        room.delete()
        return redirect('admin_management')  # Or any other appropriate URL
    return render(request, 'room_booking/delete_room.html', {'room': room})

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_management')
    else:
        form = RoomForm()
    return render(request, 'room_booking/create_room.html', {'form': form})

def user_data(request):
    total_users = User.objects.count()
    users_with_bookings = Booking.objects.values_list('user', flat=True).distinct().count()

    user_list = User.objects.all().values('username', 'first_name', 'last_name')

    data = {
        'total_users': total_users,
        'users_with_bookings': users_with_bookings,
        'user_list': user_list
    }
    return JsonResponse(data)