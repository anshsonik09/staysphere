# StaySphere - Hotel & Restaurant Management System

A modern, comprehensive hotel and restaurant management platform built with Django.

## 🌟 Features

### 🏨 Hotel Management
- Room booking system with real-time availability
- Multiple room categories (Single, Double, Deluxe, Suite)
- Check-in/Check-out management
- Customer reviews and ratings
- Occupancy reporting

### 🍽️ Restaurant Management
- Multi-cuisine menu management
- Online food ordering system
- Table reservation system
- Room delivery service
- Order status tracking

### 🏊 Facility Management
- Swimming pool, gym, spa bookings
- Time-based facility reservations
- Facility availability tracking
- Pricing management

### 💰 Billing & Finance
- Invoice generation with GST calculation
- Multiple payment methods
- Payment status tracking
- Financial reporting

### 👥 User Management
- Role-based access control (Admin, Reception, Customer)
- User profiles with role management
- Secure authentication system

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite (development), MySQL (production)
- **Authentication**: Django built-in auth
- **UI Framework**: Bootstrap 5 + Crispy Forms
- **PDF Generation**: ReportLab

## 📋 Prerequisites

- Python 3.8+
- pip package manager
- Git (optional)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd staysphere
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix/MacOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create sample data (optional)
python manage.py create_dummy_data
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 🔐 Default Login Credentials

### Admin Account
- **Username**: admin
- **Password**: (set during superuser creation)
- **Role**: Administrator

### Test Customer Account
Register a new customer account through the registration form.

## 📁 Project Structure

```
staysphere/
├── staysphere/           # Main project directory
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── accounts/            # User management app
│   ├── models.py        # UserProfile model
│   ├── views.py         # Authentication views
│   └── templates/       # Account templates
├── booking/             # Room booking app
│   ├── models.py        # Room, Booking, Review models
│   ├── views.py         # Booking views
│   └── templates/       # Booking templates
├── restaurant/          # Restaurant management app
│   ├── models.py        # Menu, Order, Table models
│   ├── views.py         # Restaurant views
│   └── templates/       # Restaurant templates
├── facilities/          # Facility management app
│   ├── models.py        # Facility, FacilityBooking models
│   ├── views.py         # Facility views
│   └── templates/       # Facility templates
├── reception/           # Reception & billing app
│   ├── models.py        # Invoice, Payment models
│   ├── views.py         # Reception views
│   └── templates/       # Reception templates
├── static/              # Static files (CSS, JS, Images)
├── media/               # Media uploads
└── templates/           # Base templates
```

## 🎯 User Roles & Permissions

### Administrator
- Full system access
- User management
- System configuration
- All CRUD operations

### Reception Staff
- Check-in/Check-out management
- Invoice generation
- Booking management
- Customer registration

### Customer
- Room booking
- Food ordering
- Facility reservations
- Profile management

## 🔧 Configuration

### Database Settings
For production, update `staysphere/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'staysphere_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Email Configuration
Update email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 📊 Available Features

### Public Website
- ✅ Home page with hero section
- ✅ Room browsing and booking
- ✅ Restaurant menu and ordering
- ✅ Facility booking
- ✅ User registration and login
- ✅ Customer dashboard

### Reception Panel
- ✅ Walk-in customer registration
- ✅ Room allotment system
- ✅ Check-in/Check-out management
- ✅ Invoice generation
- ✅ Occupancy reports

### Admin Panel
- ✅ User management
- ✅ Room management
- ✅ Menu management
- ✅ Facility management
- ✅ Billing and finance
- ✅ Comprehensive reporting

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up production database
4. Configure static files serving
5. Set up email backend
6. Configure security settings

### Static Files Collection
```bash
python manage.py collectstatic
```

## 📝 Development Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Create sample data
python manage.py create_dummy_data

# Collect static files
python manage.py collectstatic
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support and queries:
- Email: info@staysphere.com
- Phone: +91 98765 43210

## 📄 License

This project is licensed under the MIT License.

## 🎉 Acknowledgments

- Django Framework
- Bootstrap 5
- Font Awesome Icons
- ReportLab for PDF generation
