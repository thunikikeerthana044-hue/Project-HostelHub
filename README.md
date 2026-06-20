# 🏠 HostelHub — Hostel Booking & Management System

HostelHub is a modern, full-stack web application built with **Django** that simplifies the process of finding, booking, and managing hostels. It serves two types of users: **Students/Travelers** looking for a place to stay, and **Hostel Owners** looking to list their properties, manage rooms, and track bookings.

---

 Features

### 🎓 For Students (Seekers)
- **Hostel Search & Discovery**: Search hostels by city and filter by amenities or gender configuration.
- **Detailed Listings**: View comprehensive descriptions, room configurations (Single, Sharing, Dorms), pricing, security deposits, and amenities with clear visual indicators.
- **Seamless Booking System**: Reserve rooms for specific durations with automatic price calculation.
- **Razorpay Payment Integration**: Safe and secure online payments using the Razorpay gateway.
- **Interactive Ratings & Reviews**: Leave feedback and read authentic reviews from past occupants.
- **Student Dashboard**: View booking status (Pending, Confirmed, Cancelled), payment history, and profile details.

### 🏢 For Hostel Owners
- **Owner Dashboard**: A central hub to monitor total earnings, number of bookings, and active rooms.
- **Hostel & Room Management**: Easily list new hostels, upload images, specify gender types, and add/modify room configurations.
- **Booking Management**: Approve, confirm, or decline booking requests in real-time.
- **Detailed Analytics**: Check room availability and track occupant data.

---

## 🛠️ Tech Stack

- **Backend**: Django 5.x, Python 3.11
- **Database**: SQLite (default), PostgreSQL / MySQL ready (drivers included in `requirements.txt`)
- **Frontend**: Responsive HTML5, Vanilla CSS3 (Modern glassmorphism & gradients), JavaScript
- **Payment Gateway**: Razorpay API
- **Deployment**: Dockerized (`Dockerfile`, `Procfile`, and `build.sh` included for easy deployment to services like Render/Heroku)

---

## 🚀 Getting Started

### 📋 Prerequisites
Make sure you have the following installed:
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

---x

### 💻 Local Setup (Manual)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/hostelhub.git
   cd hostelhub


2. Create and Activate a Virtual Environment
# Windows
python -m venv venv
.\venv\Scripts\activate
# macOS/Linux
python3 -m venv venv
source venv/bin/activate


**Install Dependencies**
pip install -r requirements.txt


**Run Database Migrations**
python manage.py migrate


**Seed Sample Data (Optional)**
We provide a helper script to quickly seed the database with mock hostels, amenities, and users for testing:
python seed_data.py

**Start the Development Server**
python manage.py runserver
Open your browser and navigate to http://127.0.0.1:8000/.

**⚡ Easy Launch (Windows Only)**
If you are on Windows, you can simply run the launcher script:

cmd
run_project.bat
This script will automatically verify dependencies, run migrations, and spin up the server while opening the web app in your default browser.

**🔑 Pre-Configured Test Accounts**
If you use the seed_data.py script, you can log in directly using these pre-configured credentials:

Role	Username	Password
🎓 Student / Seeker	seeker	password123
🏢 Hostel Owner	owner	password123
👑 Administrator	admin	admin123 (created via superuser if needed)


**🐳 Docker Support**
HostelHub is fully containerized. To build and run the application locally using Docker:

**Build the image:**
docker build -t hostelhub .

**Run the container:**
docker run -p 8080:8080 hostelhub
Access the app at http://localhost:8080/.

**📁 Project Structure**
hostelhub/
├── accounts/          # User authentication, profiles, signup/login
├── hostels/           # Hostel listings, rooms, bookings, reviews, payment views
├── hostelhub/         # Main settings, URLs, WSGI configuration
├── media/             # Uploaded user avatars and hostel pictures
├── templates/         # Shared HTML files
├── Dockerfile         # Docker container configuration
├── requirements.txt   # Python dependency list
├── run_project.bat    # Windows automatic launch helper script
└── seed_data.py       # Script to populate database with mock listings
