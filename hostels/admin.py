# hostels/admin.py

from django.contrib import admin
from .models import UserProfile, Hostel, HostelImage, Room, Booking, Review, Amenity

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'owner', 'is_verified', 'is_active', 'created_at']
    list_filter  = ['is_verified', 'is_active', 'city', 'gender_type']
    search_fields = ['name', 'city', 'owner__username']
    list_editable = ['is_verified', 'is_active']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['hostel', 'room_type', 'price_per_month', 'available_rooms', 'is_available']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['guest', 'room', 'check_in_date', 'status', 'payment_status', 'total_amount']
    list_filter  = ['status', 'payment_status']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['hostel', 'reviewer', 'rating', 'created_at']

admin.site.register(UserProfile)
admin.site.register(Amenity)
admin.site.register(HostelImage)
