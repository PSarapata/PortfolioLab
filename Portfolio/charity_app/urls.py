from django.urls import path
from charity_app.views import LandingPage, AddDonation, ConfirmationView, Login, Logout, Register, SaveDonationView, SelectedInstitutionsView

urlpatterns = [
    path('', LandingPage.as_view(), name='Homepage'),
    path('donate/', AddDonation.as_view(), name='Donate'),
    path('donate/confirmation/', ConfirmationView.as_view(), name='Confirmation'),
    path('login/', Login.as_view(), name='Login'),
    path('logout/', Logout.as_view(), name='Logout'),
    path('register/', Register.as_view(), name='Register'),
    path('ajax/selected-institutions/', SelectedInstitutionsView.as_view(), name='Selected_Institutions'),
    path('ajax/save-donation/', SaveDonationView.as_view(), name='Save_Donation'),
]
