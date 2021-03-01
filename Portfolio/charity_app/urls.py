from django.urls import path
from charity_app.views import LandingPage, AddDonation, Login, Logout, Register, SelectedInstitutionsView

urlpatterns = [
    path('', LandingPage.as_view(), name='Homepage'),
    path('donate/',AddDonation.as_view(), name='Donate'),
    path('login/', Login.as_view(), name='Login'),
    path('logout/', Logout.as_view(), name='Logout'),
    path('register/', Register.as_view(), name='Register'),
    path('ajax/selected-institutions/', SelectedInstitutionsView.as_view(), name='Selected_Institutions')
]
