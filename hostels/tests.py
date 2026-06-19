# hostels/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from hostels.models import UserProfile, Hostel, Room

class HostelHubTests(TestCase):
    def setUp(self):
        # Create user
        self.owner_user = User.objects.create_user(username='testowner', password='password123')
        self.owner_profile = UserProfile.objects.get(user=self.owner_user)
        self.owner_profile.role = 'owner'
        self.owner_profile.save()

        # Create hostel
        self.hostel = Hostel.objects.create(
            owner=self.owner_user,
            name="Test Hostel",
            description="A test hostel description",
            address="Test street",
            city="Bangalore",
            state="Karnataka",
            pincode="560001",
            phone="1234567890",
            gender_type="mixed",
            is_verified=True,
            is_active=True
        )

        # Create room
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_type="single",
            capacity=1,
            price_per_month=5000.00,
            available_rooms=3,
            total_rooms=3,
            is_available=True
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Hostel")

    def test_hostel_search_list(self):
        response = self.client.get(reverse('hostel_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Hostel")

    def test_hostel_search_filtering(self):
        # Search by city
        response = self.client.get(reverse('hostel_list') + '?city=Bangalore')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Hostel")

        # Search by city that doesn't exist
        response = self.client.get(reverse('hostel_list') + '?city=Pune')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Hostel")

    def test_hostel_detail_page(self):
        response = self.client.get(reverse('hostel_detail', kwargs={'hostel_id': self.hostel.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Hostel")
        self.assertContains(response, "Single Room")
