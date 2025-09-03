from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name="home"),        # base URL → home page
    path('home/', views.home, name="home"),   # /home → home page
    path('login/', views.login_view, name="login"),  # login page
    path('services/', views.services, name="services"),  # services page
    path('aboutus/', views.aboutus, name="aboutus"),    # about page
    path('service_provider_login/',views.service_provider_login,name="service_provider_login"),
    path('user_login/',views.user_login,name="user_login"),
    path('user_login/user_forget/',views.user_forget,name="user_forget"),
    path("user_register/", views.user_register, name="user_register"),
     path("service_register/", views.service_register, name="service_register"),
     path("service_forget/", views.service_forget, name="service_forget"),
      path("user_forget/", views.user_forget, name="user_forget"),
    path('user_profile/',views.user_profile, name="user_profile"),
    path('service_profile/',views.service_profile,name="service_profile"),
    path('services/',views.services,name="services"),
    path('user_edit/',views.user_edit,name="user_edit"),
     path('service_edit/',views.service_edit,name="service_edit"),
    path("book/<int:garage_id>/<str:service_name>/", views.book_service, name="book_service"),
     path('garage_dashboard/',views.garage_dashboard,name="garage_dashboard"),
     path("update_booking_status/<int:booking_id>/", views.update_booking_status, name="update_booking_status"),
      path('logout/', views.logout_view, name='logout_view'),
       path("logout_sp/", views.service_provider_logout, name="service_provider_logout"),
      path("send-otp/", views.send_otp, name="send_otp"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("send-sp-otp/", views.send_sp_otp, name="send_sp_otp"),
path("verify-sp-otp/", views.verify_sp_otp, name="verify_sp_otp"),
path("reset-sp-password/", views.reset_sp_password, name="reset_sp_password"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)