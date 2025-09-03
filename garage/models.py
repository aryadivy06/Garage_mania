from django.db import models
from django.contrib.auth.models import User

# User Registration
class UserRegister(models.Model):
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=10, unique=True)  # exactly 10 digits
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # store hashed password

    # Address
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)

    # Profile photo
    profile_p = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    def __str__(self):
        return self.username

# Vehicle Model
class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('bike', 'Bike'),
        ('scooter', 'Scooter'),
        ('car', 'Car'),
        ('other', 'Other'),
    ]

    owner = models.ForeignKey(UserRegister, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    brand = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    reg_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.get_vehicle_type_display()} - {self.brand or 'N/A'} {self.model or ''} ({self.owner.username})"
    

    # Service Provider 



# Service Provider Registration



class ServiceProviderTable(models.Model):
    # Link to the Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="service_provider")

    # Business Info
    owner_name = models.CharField(max_length=100)
    garage_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)

    # Garage Details
    address = models.CharField(max_length=200)
    location = models.URLField(blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    working_hours = models.CharField(max_length=100, blank=True, null=True)

    # Services and vehicles
    SERVICES_CHOICES = [
        ('car_wash', 'Car Wash'),
        ('windshield_lightning', 'Windshield & Lightning'),
        ('painting', 'Denting & Painting'),
        ('clutch_body_parts', 'Clutch & Body Parts'),
        ('ac', 'AC Repair'),
        ('tyre', 'Tyre & Wheel Alignment'),
        ('car_inspection', 'Car Inspection'),
        ('detailing', 'Detailing Service'),
        ('suspension', 'Suspension'),
    ]
    VEHICLE_CHOICES = [
        ('two', 'Two-Wheelers'),
        ('four', 'Four-Wheelers'),
        ('heavy', 'Heavy Vehicles'),
        ('ev', 'Electric Vehicles'),
    ]
    services = models.JSONField(default=list, blank=True)
    vehicles = models.JSONField(default=list, blank=True)

    # Documents
    id_proof = models.FileField(upload_to='service_docs/', blank=True, null=True)
    garage_logo = models.ImageField(upload_to='service_docs/', blank=True, null=True)

    # About
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.garage_name} ({self.user.username})"
    

from django.utils import timezone

class Booking(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey("UserRegister", on_delete=models.CASCADE, related_name="bookings")
    garage = models.ForeignKey("ServiceProviderTable", on_delete=models.CASCADE, related_name="bookings")
    service_name = models.CharField(max_length=100)
    vehicle = models.ForeignKey("Vehicle", on_delete=models.SET_NULL, null=True, blank=True)  # if needed
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    notes = models.TextField(blank=True, null=True)  # optional: garage notes about service

    def __str__(self):
        return f"{self.service_name} - {self.user.name} ({self.status})"