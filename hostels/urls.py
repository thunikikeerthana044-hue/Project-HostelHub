# hostels/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('',                                      views.home,                  name='home'),
    path('search/',                               views.hostel_list,           name='hostel_list'),
    path('hostel/<int:hostel_id>/',               views.hostel_detail,         name='hostel_detail'),
    path('hostel/<int:hostel_id>/review/',        views.submit_review,         name='submit_review'),
    path('book/<int:room_id>/',                   views.initiate_payment,      name='initiate_payment'),
    path('payment/verify/',                       views.verify_payment,        name='verify_payment'),
    path('booking/success/<int:booking_id>/',     views.booking_success,       name='booking_success'),
    path('booking/failed/',                       views.booking_failed,        name='booking_failed'),
    path('dashboard/',                            views.student_dashboard,     name='student_dashboard'),
    
    # Owner paths
    path('owner/dashboard/',                      views.owner_dashboard,       name='owner_dashboard'),
    path('owner/hostel/add/',                     views.add_hostel,            name='add_hostel'),
    path('owner/hostel/<int:hostel_id>/room/add/',views.add_room,              name='add_room'),
    path('owner/booking/<int:booking_id>/<str:action>/', views.update_booking_status, name='update_booking_status'),
]