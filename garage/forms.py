# forms.py
from django import forms
from .models import UserRegister, Vehicle
from django.contrib.auth.hashers import make_password
from .models import ServiceProviderTable
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_pass = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = UserRegister
        fields = [
            "name",
            "contact_no",
            "email",
            "username",
            "password",
            "street_address",
            "city",
            "state",
            "pincode",
            "profile_p"
        ]

    def clean_contact_no(self):
        contact_no = self.cleaned_data.get("contact_no")
        if not contact_no.isdigit() or len(contact_no) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact_no

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if UserRegister.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if UserRegister.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_pass = cleaned_data.get("confirm_pass")

        if password and confirm_pass and password != confirm_pass:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])  # hash password
        if commit:
            user.save()
        return user


# Separate form for Vehicle
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["vehicle_type", "brand", "model", "year", "reg_number"]
        widgets = {
            "year": forms.NumberInput(attrs={"min": 1900, "max": 2100}),
        }

# Service provider Registration 

class ServiceProviderForm(forms.ModelForm):
    # Auth fields
    username = forms.CharField()
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_pass = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # Extra choice fields
    services = forms.MultipleChoiceField(
        choices=ServiceProviderTable.SERVICES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    vehicles = forms.MultipleChoiceField(
        choices=ServiceProviderTable.VEHICLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = ServiceProviderTable
        fields = [
            "owner_name", "garage_name", "phone",
            "address", "location", "license_number", "experience", "working_hours",
            "services", "vehicles", "id_proof", "garage_logo", "about"
        ]

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        cpwd = cleaned.get("confirm_pass")
        if pwd and cpwd and pwd != cpwd:
            raise ValidationError("Passwords do not match!")
        return cleaned

    def save(self, commit=True):
        # Extract auth fields
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")  # optional, if you add an email field

        # Create User
        if User.objects.filter(username=username).exists():
                raise ValidationError("Username already exists.")
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create ServiceProvider instance
        sp = super().save(commit=False)
        sp.user = user
        sp.services = self.cleaned_data.get("services", [])
        sp.vehicles = self.cleaned_data.get("vehicles", [])

        if commit:
            sp.save()
        return sp
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another one.")
        return username


class ServiceProviderLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field'}))