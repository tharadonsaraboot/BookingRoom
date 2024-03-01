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
    path('admin/profile/', admin_profile, name='admin_profile'),
    path('admin/management/', admin_management, name='admin_management'), 
    path('admin/payment_slips/', admin_payment_slips, name='admin_payment_slips'),
    path('admin/payment_slips/<int:slip_id>/verify/', verify_payment_slip, name='verify_payment_slip'),
    path('admin/profile/<int:user_id>/', view_user, name='view_user'),
    path('admin/profile/<int:user_id>/edit/', edit_user, name='edit_user'),
    path('admin/profile/<int:user_id>/delete/', delete_user, name='delete_user'),
    path('book/<int:room_id>/', view_room, name='view_room'),
    path('admin/management/<int:room_id>/edit/', edit_room, name='edit_room'),
    path('admin/management/<int:room_id>/delete/', delete_room, name='delete_room'),
    path('admin/management/room/create/', create_room, name='create_room'),
    path('admin/profile/add_user/', add_user, name='add_user'),
    path('view_user/<int:user_id>/', view_user, name='view_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('user_profile/<int:user_id>/', user_profile, name='user_profile'),
    # fetch data
    path('user-data/', user_data, name='user-data') 
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)