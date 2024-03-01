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
                    return redirect('home')  
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
        start_date = timezone.now()  # Use current time as the start date
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.start_date = start_date
            booking.save()
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

@login_required
def payment_page(request, room_id):
    # Retrieve the Room instance by ID or return a 404
    room = get_object_or_404(Room, pk=room_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract the uploaded file and calculate the payment amount
            uploaded_file = form.cleaned_data['slip']
            payment_amount = room.earnest_money + room.prize

            # Create PaymentSlip instance and mark it as unverified
            PaymentSlip.objects.create(
                user=request.user,
                room=room,
                slip=uploaded_file,
                verified=False
            )

            # Calculate and store the countdown end time in the session
            countdown_end = timezone.now() + timedelta(minutes=10)
            request.session['countdown_end'] = countdown_end.isoformat()

            # Redirect to the waiting verification page and pass the room_id
            return render(request, 'room_booking/waiting_verification.html', {'room_id': room_id})
        else:
            # If the form is not valid, display an error message
            messages.error(request, 'There was an error with your submission. Please check your data and try again.')
    else:
        form = PaymentForm()

    # Calculate payment amount for GET requests or in case of form errors
    payment_amount = room.earnest_money + room.prize

    # Prepare the context with the form, payment amount, and sample bank details
    context = {
        'form': form,
        'payment_amount': payment_amount,
        'bank_details': 'Bank Name: ABC Bank\nAccount Number: 123456789',  # Sample bank details
        'room_id': room_id  # Make sure to include room_id in the context for the template
    }

    # Render the payment page template with the context
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
    return redirect('admin_payment_slips')

def check_payment_status(request, room_id):
    # Use filter() to get a queryset and then first() to get a single instance or None
    payment_slip = PaymentSlip.objects.filter(room_id=room_id, user=request.user).first()
    
    if payment_slip:
        return JsonResponse({'is_verified': payment_slip.verified})
    else:
        return JsonResponse({'error': 'Payment slip not found'}, status=404)

@user_passes_test(lambda u: u.is_staff) 
def admin_dashboard(request):
    # ... Logic for admin view ...
    return render(request, 'room_booking/admin_dashboard.html')

@user_passes_test(lambda u: u.is_staff) 
def admin_statistics(request):
    # ... Logic for admin view ...
    return render(request, 'room_booking/admin_statistics.html')

# def admin_payment_slips(request):
#     payment_slips = PaymentSlip.objects.filter(verified=False)
#     return render(request, 'room_booking/admin_payment_slips.html', {'payment_slips': payment_slips})

# def view_payment_slip(request, slip_id):
#     payment_slip = get_object_or_404(PaymentSlip, id=slip_id)
#     return render(request, 'room_booking/view_payment_slip.html', {'payment_slip': payment_slip})
