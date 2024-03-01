from django.conf import settings
from django.urls import path
from room_booking.views import *
from django.conf.urls.static import static

urlpatterns = [
    # Authentication
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Room Views
    path('', room_list, name='room_list'),
    path('room/<int:room_id>/', room_details, name='room_details'),

    # Booking 
    path('book/<int:room_id>/', book_room, name='book_room'),
    path('booking/success/', booking_success, name='booking_success'),
    path('booking/history/', booking_history, name='booking_history'),

    # Payment
    path('payment/<int:room_id>/', payment_page, name='payment_page'),
    path('check-payment-status/<int:room_id>/', check_payment_status, name='check_payment_status'), 

    # Admin
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/statistics/', admin_statistics, name='admin_statistics'), 
    path('admin/payment_slips/', admin_payment_slips, name='admin_payment_slips'),
    path('admin/payment_slips/<int:slip_id>/verify/', verify_payment_slip, name='verify_payment_slip'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)