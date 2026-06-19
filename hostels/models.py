# hostels/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# ─── User Profile ────────────────────────────────────────────────────────────
# Extends Django's built-in User with extra fields

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student / Traveler'),
        ('owner',   'Hostel Owner'),
    ]

    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone      = models.CharField(max_length=15, blank=True)
    city       = models.CharField(max_length=100, blank=True)
    avatar     = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def is_owner(self):
        return self.role == 'owner'


# ─── Amenity ─────────────────────────────────────────────────────────────────
# Things like WiFi, AC, Food, Laundry — reused across hostels

class Amenity(models.Model):
    name = models.CharField(max_length=50)  # e.g. "WiFi", "AC", "Hot Water"
    icon = models.CharField(max_length=50, blank=True)  # CSS/icon class name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"


# ─── Hostel ──────────────────────────────────────────────────────────────────

class Hostel(models.Model):
    GENDER_CHOICES = [
        ('male',   'Male Only'),
        ('female', 'Female Only'),
        ('mixed',  'Mixed / Co-ed'),
    ]

    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hostels')
    name        = models.CharField(max_length=200)
    description = models.TextField()
    address     = models.TextField()
    city        = models.CharField(max_length=100)
    state       = models.CharField(max_length=100)
    pincode     = models.CharField(max_length=10)
    phone       = models.CharField(max_length=15)
    email       = models.EmailField(blank=True)
    gender_type = models.CharField(max_length=10, choices=GENDER_CHOICES, default='mixed')
    amenities   = models.ManyToManyField(Amenity, blank=True)
    latitude    = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude   = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # admin approves
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

    def get_min_price(self):
        """Returns the cheapest room price for display"""
        rooms = self.rooms.filter(is_available=True)
        if rooms.exists():
            return rooms.order_by('price_per_month').first().price_per_month
        return None

    def get_avg_rating(self):
        """Calculates average star rating from reviews"""
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            return round(total / reviews.count(), 1)
        return None

    def get_main_image(self):
        """Returns the first/main photo"""
        img = self.images.filter(is_main=True).first()
        if not img:
            img = self.images.first()
        return img

    class Meta:
        ordering = ['-created_at']


# ─── Hostel Images ───────────────────────────────────────────────────────────
# Multiple photos per hostel

class HostelImage(models.Model):
    hostel  = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='images')
    image   = models.ImageField(upload_to='hostels/')
    caption = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)  # the cover photo

    def __str__(self):
        return f"Image for {self.hostel.name}"


# ─── Room ────────────────────────────────────────────────────────────────────

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single',  'Single Room'),
        ('double',  'Double Sharing'),
        ('triple',  'Triple Sharing'),
        ('dormitory', 'Dormitory (4+ beds)'),
    ]

    hostel          = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_type       = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    capacity        = models.PositiveIntegerField(default=1)  # number of beds
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2)
    deposit_amount  = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_rooms     = models.PositiveIntegerField(default=1)  # how many of this type
    available_rooms = models.PositiveIntegerField(default=1)
    is_available    = models.BooleanField(default=True)
    description     = models.TextField(blank=True)

    def __str__(self):
        return f"{self.hostel.name} - {self.get_room_type_display()}"


# ─── Booking ─────────────────────────────────────────────────────────────────

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    guest          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room           = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date  = models.DateField()
    check_out_date = models.DateField()
    status         = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    total_amount   = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id     = models.CharField(max_length=200, blank=True)  # Razorpay ID
    payment_status = models.CharField(max_length=20, default='unpaid')
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    special_requests = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest.username} → {self.room.hostel.name}"

    def get_duration_months(self):
        delta = self.check_out_date - self.check_in_date
        return round(delta.days / 30, 1)

    class Meta:
        ordering = ['-created_at']


# ─── Review ──────────────────────────────────────────────────────────────────

class Review(models.Model):
    hostel     = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='reviews')
    reviewer   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating     = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} rated {self.hostel.name} — {self.rating}/5"

    class Meta:
        # One review per user per hostel
        unique_together = ('hostel', 'reviewer')
        ordering = ['-created_at']

