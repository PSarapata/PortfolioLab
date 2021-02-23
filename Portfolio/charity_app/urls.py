from django.urls import path
from charity_app.views import LandingPage, AddDonation, Login, Register

urlpatterns = [
    path('', LandingPage.as_view(), name='Landing Page'),
    path('donate/',AddDonation.as_view(), name='Make a Donation'),
    path('login/', Login.as_view(), name='Login'),
    path('register/', Register.as_view(), name='Register')
]
