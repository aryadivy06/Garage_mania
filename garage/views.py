from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import UserRegister, Vehicle
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from .forms import ServiceProviderForm
from garage.models import ServiceProviderTable
from .forms import ServiceProviderLoginForm
# ----------------- Home -----------------
def home(request):
    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserRegister.objects.get(id=user_id)
        except UserRegister.DoesNotExist:
            request.session.flush()  # clear invalid session
            user = None
    return render(request, "home.html", {"user": user})

# ----------------- Login & Logout -----------------
def login_view(request):
    return render(request, "login.html")

def user_login(request):
    if request.method == "POST":
        login_id = request.POST.get("login_id")
        password = request.POST.get("password")

        try:
            user = UserRegister.objects.get(
                Q(username=login_id) | Q(email=login_id) | Q(contact_no=login_id)
            )
        except UserRegister.DoesNotExist:
            messages.error(request, "User not found")
            return redirect("login")

        # Secure check with hashed password
        if check_password(password, user.password):
            request.session['user_id'] = user.id
            return redirect("home")
        else:
            messages.error(request, "Invalid password")
            return redirect("login")

    return render(request, "user_login.html")

def logout_view(request):
    request.session.flush()
    return redirect("home")

# ----------------- Forget Password (User) -----------------


def user_forget(request):
    return render(request, "user_forget.html")


def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            identifier = data.get("identifier")

            user = (
                UserRegister.objects.filter(email=identifier).first()
                or UserRegister.objects.filter(username=identifier).first()
                or UserRegister.objects.filter(contact_no=identifier).first()
            )
            if not user:
                return JsonResponse({"success": False, "message": "User not found!"})

            generated_otp = str(random.randint(1000, 9999))
            request.session["reset_user"] = user.id
            request.session["reset_otp"] = generated_otp

            # Send OTP by email
            send_mail(
                "Your OTP for Password Reset",
                f"Your OTP is {generated_otp}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return JsonResponse({"success": True, "message": "OTP sent successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})


def verify_otp(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        otp = data.get("otp")

        saved_otp = request.session.get("reset_otp")
        if otp == saved_otp:
            return JsonResponse({"success": True, "message": "OTP verified."})
        return JsonResponse({"success": False, "message": "Invalid OTP!"})

    return JsonResponse({"success": False, "message": "Invalid request method."})


def reset_password(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            return JsonResponse({"success": False, "message": "Passwords do not match!"})

        user_id = request.session.get("reset_user")
        if not user_id:
            return JsonResponse({"success": False, "message": "Session expired. Try again."})

        try:
            user = UserRegister.objects.get(id=user_id)
        except UserRegister.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found."})

        user.password = make_password(password1)
        user.save()

        # clear session
        request.session.pop("reset_user", None)
        request.session.pop("reset_otp", None)

        return JsonResponse({"success": True, "message": "Password updated successfully."})

    return JsonResponse({"success": False, "message": "Invalid request method."})


# ----------------- Forget Password (Service Provider) -----------------
def service_forget(request):
    return render(request, "service_forget.html")


def send_sp_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            identifier = data.get("identifier")

            # Search service provider by email, username, or phone
            sp = (
                ServiceProviderTable.objects.filter(user__email=identifier).first()
                or ServiceProviderTable.objects.filter(user__username=identifier).first()
                or ServiceProviderTable.objects.filter(phone=identifier).first()
            )
            if not sp:
                return JsonResponse({"success": False, "message": "Service provider not found!"})

            generated_otp = str(random.randint(1000, 9999))
            request.session["reset_sp"] = sp.id
            request.session["reset_sp_otp"] = generated_otp

            # Send OTP by email
            send_mail(
                "Your OTP for Garage Mania (Service Provider)",
                f"Your OTP is {generated_otp}",
                settings.DEFAULT_FROM_EMAIL,
                [sp.user.email],
                fail_silently=False,
            )

            return JsonResponse({"success": True, "message": "OTP sent successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})


def verify_sp_otp(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        otp = data.get("otp")

        saved_otp = request.session.get("reset_sp_otp")
        if otp == saved_otp:
            return JsonResponse({"success": True, "message": "OTP verified."})
        return JsonResponse({"success": False, "message": "Invalid OTP!"})

    return JsonResponse({"success": False, "message": "Invalid request method."})


def reset_sp_password(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 != password2:
            return JsonResponse({"success": False, "message": "Passwords do not match!"})

        sp_id = request.session.get("reset_sp")
        if not sp_id:
            return JsonResponse({"success": False, "message": "Session expired. Try again."})

        try:
            sp = ServiceProviderTable.objects.get(id=sp_id)
        except ServiceProviderTable.DoesNotExist:
            return JsonResponse({"success": False, "message": "Service provider not found."})

        # Update password in User model linked to ServiceProviderTable
        sp.user.password = make_password(password1)
        sp.user.save()

        # clear session
        request.session.pop("reset_sp", None)
        request.session.pop("reset_sp_otp", None)

        return JsonResponse({"success": True, "message": "Password updated successfully."})

    return JsonResponse({"success": False, "message": "Invalid request method."})
# ----------------- Registration -----------------
def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()

            # Save two-wheelers
            two_wheelers_count = int(request.POST.get('two_wheelers', 0))
            for i in range(1, two_wheelers_count + 1):
                brand = request.POST.get(f'two-wheeler_name_{i}')
                model = request.POST.get(f'two-wheeler_model_{i}')
                if brand or model:
                    Vehicle.objects.create(
                        owner=user,
                        vehicle_type='bike',
                        brand=brand,
                        model=model
                    )

            # Save four-wheelers
            four_wheelers_count = int(request.POST.get('four_wheelers', 0))
            for i in range(1, four_wheelers_count + 1):
                brand = request.POST.get(f'four-wheeler_name_{i}')
                model = request.POST.get(f'four-wheeler_model_{i}')
                if brand or model:
                    Vehicle.objects.create(
                        owner=user,
                        vehicle_type='car',
                        brand=brand,
                        model=model
                    )

            messages.success(request, "Registration successful. Please login.")
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "user_register.html", {"form": form})

def service_register(request):
    if request.method == "POST":
        form = ServiceProviderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service Provider registration successful. Please login.")
            return redirect("login")
    else:
        form = ServiceProviderForm()

    return render(request, "service_register.html", {"form": form})
# ----------------- Profiles -----------------
def user_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = UserRegister.objects.get(id=user_id)
    except UserRegister.DoesNotExist:
        request.session.flush()
        return redirect('login')

    vehicles = user.vehicles.all()
    two_wheelers = vehicles.filter(vehicle_type__in=['bike', 'scooter'])
    four_wheelers = vehicles.filter(vehicle_type__in=['car', 'other'])

    return render(request, "user_profile.html", {
        "user": user,
        "two_wheeler_list": two_wheelers,
        "four_wheeler_list": four_wheelers
    })


# ----------------- Edit Profiles -----------------
def user_edit(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = UserRegister.objects.get(id=user_id)

    if request.method == "POST":
        # Update user info
        user.name = request.POST.get('name', user.name)
        user.contact_no = request.POST.get('contact_no', user.contact_no)
        user.email = request.POST.get('email', user.email)
        if 'profile_p' in request.FILES:
            user.profile_p = request.FILES['profile_p']
        user.save()

        # Update existing vehicles
        vehicle_count = int(request.POST.get('vehicle_count', 0))
        for i in range(1, vehicle_count + 1):
            vid = request.POST.get(f'vehicle_id_{i}')
            if vid:
                vehicle = Vehicle.objects.get(id=vid, owner=user)
                vehicle.brand = request.POST.get(f'vehicle_brand_{i}', '')
                vehicle.model = request.POST.get(f'vehicle_model_{i}', '')
                year = request.POST.get(f'vehicle_year_{i}')
                vehicle.year = int(year) if year else None
                vehicle.reg_number = request.POST.get(f'vehicle_reg_{i}', '')
                vehicle.save()

        # Add new vehicles
        new_vehicle_count = int(request.POST.get('new_vehicle_count', 0))
        for i in range(1, new_vehicle_count + 1):
            vtype = request.POST.get(f'new_vehicle_type_{i}')
            brand = request.POST.get(f'new_vehicle_brand_{i}')
            model = request.POST.get(f'new_vehicle_model_{i}')
            year = request.POST.get(f'new_vehicle_year_{i}')
            reg_no = request.POST.get(f'new_vehicle_reg_{i}')
            if vtype and (brand or model):
                Vehicle.objects.create(
                    owner=user,
                    vehicle_type=vtype,
                    brand=brand,
                    model=model,
                    year=int(year) if year else None,
                    reg_number=reg_no
                )

        messages.success(request, "Profile updated successfully.")
        return redirect('user_profile')

    vehicles = user.vehicles.all()
    return render(request, "user_edit.html", {"user": user, "vehicles": vehicles})
@login_required
def service_edit(request):
    try:
        profile = request.user.service_provider  # if related_name="service_provider"
    except AttributeError:
        profile = request.user.serviceprovidertable  # fallback if related_name not set

    user = profile.user  # linked Django User object

    if request.method == "POST":
        # Update User fields
        new_email = request.POST.get("email", user.email)
        new_username = request.POST.get("username", user.username)

        user.email = new_email
        user.username = new_username
        user.save()  # ✅ save User model changes

        # Update ServiceProvider fields
        profile.owner_name = request.POST.get("owner", profile.owner_name)
        profile.garage_name = request.POST.get("business_name", profile.garage_name)
        profile.phone = request.POST.get("phone", profile.phone)
        profile.address = request.POST.get("address", profile.address)
        profile.location = request.POST.get("location", profile.location)
        profile.license_number = request.POST.get("license", profile.license_number)
        profile.experience = request.POST.get("experience", profile.experience)
        profile.working_hours = request.POST.get("hours", profile.working_hours)
        profile.about = request.POST.get("about", profile.about)

        # Handle services (checkbox group)
        services = request.POST.getlist("services")
        if services:
            profile.services = services  

        # Handle vehicles (checkbox group)
        vehicles = request.POST.getlist("vehicles")
        if vehicles:
            profile.vehicles = vehicles  

        # File uploads
        if "garage_logo" in request.FILES:
            profile.garage_logo = request.FILES["garage_logo"]

        if "id_proof" in request.FILES:
            profile.id_proof = request.FILES["id_proof"]

        # Save ServiceProvider changes
        profile.save()

        return redirect("service_profile")

    return render(request, "service_edit.html", {"profile": profile, "user": user})

# ----------------- Misc Pages -----------------
def services(request):
    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserRegister.objects.get(id=user_id)
        except UserRegister.DoesNotExist:
            request.session.flush()
            user = None

    garages = ServiceProviderTable.objects.all()

    # mapping service keys (from DB) to image filenames
    service_images = {
        "car_wash": "carwash.jpg",
        "windshield_lightning": "windshield.jpg",
        "painting": "painting.png",              # Denting & Painting
        "clutch_body_parts": "clutch.jpg",   # Clutch & Body Parts
        "ac": "ac.jpg",                      # AC Repair
        "tyre": "tyres.jpg",                 # Tyre & Wheel Alignment
        "car_inspection": "inspection.jpg",  # Car Inspection
        "detailing": "detailing.jpg",        # Detailing Service
        "suspension": "suspension.jpg",      # Suspension
    }

    selected_garage_id = request.GET.get("garage_id")
    services_list = []

    if selected_garage_id:
        garage = get_object_or_404(ServiceProviderTable, id=selected_garage_id)
        if garage.services:
            for service in garage.services:
                services_list.append({
                    "service_name": service,
                    "garage": garage,
                    "image": service_images.get(service, "default.jpg")
                })
    else:
        for garage in garages:
            if garage.services:
                for service in garage.services:
                    services_list.append({
                        "service_name": service,
                        "garage": garage,
                        "image": service_images.get(service, "default.jpg")
                    })

    return render(request, "services.html", {
        "user": user,
        "garages": garages,
        "services_list": services_list,
        "selected_garage_id": selected_garage_id,
    })


def aboutus(request):
    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserRegister.objects.get(id=user_id)
        except UserRegister.DoesNotExist:
            request.session.flush()
            user = None
    return render(request, "aboutus.html", {"user": user})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import UserRegister, ServiceProviderTable, Vehicle, Booking

from django.core.mail import send_mail
from django.conf import settings

def book_service(request, garage_id, service_name):
    user_id = request.session.get("user_id")
    if not user_id:
        messages.error(request, "You need to log in to book a service.")
        return redirect("login")

    user = get_object_or_404(UserRegister, id=user_id)
    garage = get_object_or_404(ServiceProviderTable, id=garage_id)

    # Step 1: Show vehicle selection page
    if request.method == "GET":
        vehicles = Vehicle.objects.filter(owner=user)
        if not vehicles.exists():
            messages.error(request, "Please add a vehicle before booking a service.")
            return redirect("user_profile")

        return render(request, "select_vehicle.html", {
            "vehicles": vehicles,
            "garage": garage,
            "service_name": service_name,
        })

    # Step 2: Handle POST (user selects vehicle)
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle_id")
        vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=user)

        booking = Booking.objects.create(
            user=user,
            garage=garage,
            service_name=service_name,
            vehicle=vehicle,
            date=timezone.now(),
            status="Pending"
        )

        # ✅ Send email notification to service provider
        if garage.user.email:  # use linked Django user email
            subject = f"New Booking - {service_name}"
            message = (
                f"Hello {garage.garage_name},\n\n"
                f"You have received a new booking request.\n\n"
                f"🔧 Service: {service_name}\n"
                f"🚗 Vehicle: {vehicle.get_vehicle_type_display()} - {vehicle.brand} {vehicle.model} ({vehicle.reg_number})\n"
                f"👤 Customer: {user.username} ({user.email})\n"
                f"📅 Date: {booking.date.strftime('%d/%m/%Y %H:%M')}\n\n"
                f"Please log in to your dashboard to manage this request.\n\n"
                f"Regards,\nGarage Mania"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [garage.user.email],  # ✅ service provider’s email from linked Django user
                fail_silently=False,
            )

        messages.success(
            request,
            f"{service_name} booked successfully for {vehicle.brand or vehicle.get_vehicle_type_display()}!"
        )
        return redirect(f"/services/?garage_id={garage_id}")

def service_provider_login(request):
    if request.method == "POST":
        userid = request.POST.get("userid")
        password = request.POST.get("password")

        try:
            # find user by username OR email OR phone
            user = User.objects.filter(
                Q(username=userid) | Q(email=userid) | Q(service_provider__phone=userid)
            ).first()

            if user:
                auth_user = authenticate(request, username=user.username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    sp = auth_user.service_provider  # linked ServiceProvider
                    messages.success(request, f"Welcome {sp.garage_name}!")
                    return redirect("garage_dashboard")   # ✅ redirect to dashboard
                else:
                    messages.error(request, "Incorrect password!")
            else:
                messages.error(request, "Username / Email / Phone does not exist!")
        except Exception as e:
            messages.error(request, f"Login error: {e}")

    return render(request, "service_provider_login.html")


from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def service_profile(request):
    """
    Display the logged-in service provider's profile.
    Always pulls the fresh User instance linked to the ServiceProvider.
    """
    sp = getattr(request.user, "service_provider", None) or getattr(request.user, "serviceprovidertable", None)

    if not sp:
        return render(request, "service_profile.html", {
            "error": "No service provider profile found."
        })

    # Reload the linked User object to ensure updated email/username appear
    user = User.objects.get(id=sp.user.id)

    return render(request, "service_profile.html", {
        "provider": sp,
        "user": user,   # fresh user object
    })



@login_required
def garage_dashboard(request):
    try:
        service_provider = request.user.service_provider  # linked to Django User
    except ServiceProviderTable.DoesNotExist:
        messages.error(request, "You are not registered as a service provider.")
        return redirect("home")

    # Fetch all bookings for this garage
    bookings = Booking.objects.filter(garage=service_provider).order_by("-date")

    # ✅ Stats
    completed_count = bookings.filter(status="Completed").count()
    pending_count = bookings.filter(status__in=["Pending", "In Progress"]).count()
    customers_count = bookings.values("user").distinct().count()

    return render(request, "garage_dashboard.html", {
        "service_provider": service_provider,
        "bookings": bookings,
        "completed_count": completed_count,
        "pending_count": pending_count,
        "customers_count": customers_count,
    })


# ✅ Update Booking Status + Send Email
@login_required
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, garage=request.user.service_provider)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status not in dict(Booking.STATUS_CHOICES):
            messages.error(request, "Invalid status selected.")
            return redirect("garage_dashboard")

        booking.status = new_status
        booking.save()

        # ✅ Send Email to User
        subject = f"Service Status Update - {booking.service_name}"
        message = (
            f"Hello {booking.user.name},\n\n"
            f"Your service '{booking.service_name}' with {booking.garage.garage_name} "
            f"has been updated to: {booking.status}.\n\n"
            f"Thank you for using Garage Mania!"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [booking.user.email], fail_silently=True)

        messages.success(request, f"Booking status updated to {new_status} and user notified.")
        return redirect("garage_dashboard")

    return redirect("garage_dashboard")


def service_provider_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("service_provider_login")



