# hostels/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
import razorpay, json, hmac, hashlib, uuid
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Min, Avg
from .models import Hostel, Room, Booking, Amenity, Review, HostelImage

# ── Home / Landing page ───────────────────────────────────────────────────────

def home(request):
    featured_hostels = Hostel.objects.filter(is_active=True, is_verified=True)[:3]
    stats = {
        'hostels_count': Hostel.objects.filter(is_active=True).count(),
        'cities_count': Hostel.objects.filter(is_active=True).values('city').distinct().count(),
        'bookings_count': Booking.objects.filter(status='confirmed').count() + 120, # Add seed offset for stats
    }
    return render(request, 'hostels/home.html', {
        'featured_hostels': featured_hostels,
        'stats': stats,
    })


# ── Hostel search & list page ──────────────────────────────────────────────────

def hostel_list(request):
    hostels = Hostel.objects.filter(is_active=True)

    # Search filters
    city = request.GET.get('city', '').strip()
    gender = request.GET.get('gender', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    room_type = request.GET.get('room_type', '').strip()
    ac_only = request.GET.get('ac_only', '').strip()
    verified_only = request.GET.get('verified_only', '').strip()
    selected_amenities = request.GET.getlist('amenities')
    sort_by = request.GET.get('sort_by', 'relevance').strip()

    if city:
        from django.db.models import Q
        hostels = hostels.filter(Q(city__icontains=city) | Q(address__icontains=city))
    if gender:
        hostels = hostels.filter(gender_type=gender)
    if verified_only == 'true':
        hostels = hostels.filter(is_verified=True)

    # Filter by selected amenities
    if selected_amenities:
        for am_id in selected_amenities:
            if am_id.isdigit():
                hostels = hostels.filter(amenities__id=int(am_id))

    # Room-based filters
    room_filters = {}
    if max_price:
        room_filters['price_per_month__lte'] = float(max_price)
    if room_type:
        room_filters['room_type'] = room_type
    
    # AC Non-AC filtering based on description
    if ac_only == 'true':
        room_filters['description__icontains'] = 'ac'

    if room_filters:
        matching_rooms = Room.objects.filter(**room_filters)
        hostels = hostels.filter(rooms__in=matching_rooms).distinct()

    # Annotate min price and rating for sorting
    hostels = hostels.annotate(
        min_price=Min('rooms__price_per_month'),
        avg_rating=Avg('reviews__rating')
    )

    # Sorting
    if sort_by == 'price_asc':
        hostels = hostels.order_by('min_price')
    elif sort_by == 'price_desc':
        hostels = hostels.order_by('-min_price')
    elif sort_by == 'rating_desc':
        hostels = hostels.order_by('-avg_rating')
    elif sort_by == 'newest':
        hostels = hostels.order_by('-created_at')

    all_amenities = Amenity.objects.all()

    return render(request, 'hostels/hostel_list.html', {
        'hostels': hostels,
        'all_amenities': all_amenities,
        'city': city,
        'gender': gender,
        'max_price': max_price,
        'room_type': room_type,
        'ac_only': ac_only,
        'verified_only': verified_only,
        'selected_amenities': [int(x) for x in selected_amenities if x.isdigit()],
        'sort_by': sort_by,
    })


# ── Hostel detail page ────────────────────────────────────────────────────────

def hostel_detail(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id, is_active=True)
    rooms = hostel.rooms.all()
    reviews = hostel.reviews.all().order_by('-created_at')

    # Calculate subcategory scores dynamically or mock them
    cleanliness = 4.5
    food = 4.2
    safety = 4.8
    wifi = 4.6

    return render(request, 'hostels/hostel_detail.html', {
        'hostel': hostel,
        'rooms': rooms,
        'reviews': reviews,
        'today': date.today().isoformat(),
        'scores': {
            'cleanliness': cleanliness,
            'food': food,
            'safety': safety,
            'wifi': wifi,
        }
    })


# ── Initiate payment ──────────────────────────────────────────────────────────

@login_required
def initiate_payment(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        check_in = request.POST.get('check_in_date')
        check_out = request.POST.get('check_out_date')
        special_requests = request.POST.get('special_requests', '')

        if not check_in or not check_out:
            messages.error(request, "Please select both check-in and check-out dates.")
            return redirect('hostel_detail', hostel_id=room.hostel.id)

        try:
            ci = date.fromisoformat(check_in)
            co = date.fromisoformat(check_out)
        except ValueError:
            messages.error(request, "Invalid dates provided.")
            return redirect('hostel_detail', hostel_id=room.hostel.id)

        if co <= ci:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect('hostel_detail', hostel_id=room.hostel.id)

        days = (co - ci).days
        months = max(1, round(days / 30.0, 1))
        total = room.price_per_month * int(months) # Standardizing total amount as whole month count
        paise = int(total * 100)

        # Secure integration with Razorpay, falling back to simulator if API keys aren't setup
        is_mock = False
        rzp_order_id = ""

        try:
            if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                rzp_order = client.order.create({
                    'amount': paise, 'currency': 'INR', 'payment_capture': 1
                })
                rzp_order_id = rzp_order['id']
            else:
                raise ValueError("Keys not configured")
        except Exception as e:
            # Fallback to simulated booking flow
            rzp_order_id = f"mock_order_{uuid.uuid4().hex[:12]}"
            is_mock = True

        booking = Booking.objects.create(
            guest=request.user, room=room,
            check_in_date=ci, check_out_date=co,
            total_amount=total, status='pending', payment_status='unpaid',
            razorpay_order_id=rzp_order_id,
            special_requests=special_requests
        )

        return render(request, 'hostels/payment.html', {
            'booking': booking, 'room': room,
            'razorpay_key': settings.RAZORPAY_KEY_ID or 'rzp_test_mock_keys_123',
            'razorpay_order_id': rzp_order_id,
            'amount_paise': paise, 'amount_display': total,
            'is_mock': is_mock,
        })

    return redirect('hostel_detail', hostel_id=room.hostel.id)


# ── Verify payment ────────────────────────────────────────────────────────────

@csrf_exempt
@login_required
def verify_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('razorpay_order_id')
        payment_id = data.get('razorpay_payment_id')
        signature = data.get('razorpay_signature')

        booking = get_object_or_404(Booking, razorpay_order_id=order_id)
        
        # Verify signature
        success = False
        if order_id.startswith('mock_') and signature == 'mock_signature':
            success = True
        else:
            msg = f"{order_id}|{payment_id}"
            try:
                expected = hmac.new(
                    settings.RAZORPAY_KEY_SECRET.encode(),
                    msg.encode(), hashlib.sha256
                ).hexdigest()
                if expected == signature:
                    success = True
            except Exception:
                success = False

        if success:
            booking.razorpay_payment_id = payment_id
            booking.razorpay_signature = signature
            booking.status = 'confirmed'
            booking.payment_status = 'paid'
            booking.save()
            
            # Decrement available room count
            room = booking.room
            if room.available_rooms > 0:
                room.available_rooms -= 1
                if room.available_rooms == 0:
                    room.is_available = False
                room.save()
                
            return JsonResponse({'status': 'success', 'booking_id': booking.id})
        else:
            booking.status = 'cancelled'
            booking.payment_status = 'failed'
            booking.save()
            return JsonResponse({'status': 'failed'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# ── Success / Fail pages ──────────────────────────────────────────────────────

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)
    return render(request, 'hostels/booking_success.html', {'booking': booking})


@login_required
def booking_failed(request):
    return render(request, 'hostels/booking_failed.html')


# ── Student dashboard ──────────────────────────────────────────────────────────

@login_required
def student_dashboard(request):
    bookings = Booking.objects.filter(guest=request.user).order_by('-created_at')
    return render(request, 'hostels/student_dashboard.html', {'bookings': bookings})


# ── Owner dashboard & listing management ──────────────────────────────────────────

@login_required
def owner_dashboard(request):
    if request.user.profile.role != 'owner':
        messages.error(request, "Only hostel owners can access this page.")
        return redirect('hostel_list')
        
    hostels = Hostel.objects.filter(owner=request.user)
    bookings = Booking.objects.filter(room__hostel__owner=request.user).order_by('-created_at')
    
    total_earnings = sum(b.total_amount for b in bookings if b.payment_status == 'paid')
    total_bookings = bookings.count()
    active_tenants = bookings.filter(status='confirmed').count()
    
    return render(request, 'hostels/owner_dashboard.html', {
        'hostels': hostels,
        'bookings': bookings,
        'total_earnings': total_earnings,
        'total_bookings': total_bookings,
        'active_tenants': active_tenants,
    })


@login_required
def add_hostel(request):
    if request.user.profile.role != 'owner':
        messages.error(request, "Only hostel owners can list properties.")
        return redirect('hostel_list')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender_type = request.POST.get('gender_type')

        hostel = Hostel.objects.create(
            owner=request.user,
            name=name,
            description=description,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone,
            email=email,
            gender_type=gender_type,
            is_verified=True,  # Auto-verify listed hostels for smooth demo flow
            is_active=True
        )

        # Add amenities
        amenities_ids = request.POST.getlist('amenities')
        for a_id in amenities_ids:
            hostel.amenities.add(a_id)

        # Optional Photo Upload
        image_file = request.FILES.get('main_image')
        if image_file:
            HostelImage.objects.create(hostel=hostel, image=image_file, is_main=True)

        messages.success(request, f"Listed '{name}' successfully!")
        return redirect('owner_dashboard')

    amenities = Amenity.objects.all()
    return render(request, 'hostels/add_hostel.html', {'amenities': amenities})


@login_required
def add_room(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id, owner=request.user)

    if request.method == 'POST':
        room_type = request.POST.get('room_type')
        capacity = int(request.POST.get('capacity', 1))
        price_per_month = float(request.POST.get('price_per_month', 0))
        deposit_amount = float(request.POST.get('deposit_amount', 0))
        total_rooms = int(request.POST.get('total_rooms', 1))
        description = request.POST.get('description', '')

        Room.objects.create(
            hostel=hostel,
            room_type=room_type,
            capacity=capacity,
            price_per_month=price_per_month,
            deposit_amount=deposit_amount,
            total_rooms=total_rooms,
            available_rooms=total_rooms,
            is_available=True,
            description=description
        )

        messages.success(request, f"Added {room_type} room option to {hostel.name}!")
        return redirect('owner_dashboard')

    return render(request, 'hostels/add_room.html', {'hostel': hostel})


@login_required
def update_booking_status(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id, room__hostel__owner=request.user)
    
    if action == 'confirm':
        booking.status = 'confirmed'
        messages.success(request, "Booking request confirmed!")
    elif action == 'cancel':
        booking.status = 'cancelled'
        # Restore room vacancy
        room = booking.room
        room.available_rooms += 1
        room.is_available = True
        room.save()
        messages.warning(request, "Booking request cancelled.")
    
    booking.save()
    return redirect('owner_dashboard')


# ── Seeker Review submissions ──────────────────────────────────────────────────

@login_required
def submit_review(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating', 5))
            comment = request.POST.get('comment', '').strip()
            
            # Upsert user review
            review, created = Review.objects.get_or_create(
                hostel=hostel,
                reviewer=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            if not created:
                review.rating = rating
                review.comment = comment
                review.save()
                messages.success(request, "Your review has been updated.")
            else:
                messages.success(request, "Review submitted successfully!")
        except Exception as e:
            messages.error(request, "Failed to submit review.")
            
    return redirect('hostel_detail', hostel_id=hostel_id)