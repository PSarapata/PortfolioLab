from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
from django.db.models import Count
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django import template
import json
from charity_app.models import Category, Donation, Institution

User = get_user_model()
register = template.Library()

class LandingPage(View):
    def get(self, request):

        # Calculates total amount of donated bags
        def get_total_donation_qty():

            donations = Donation.objects.all()
            total = 0

            for donation in donations:
                total += donation.quantity

            return str(total)

        # Calculates total amount of supported institutions
        def get_institution_count():
            supported_institutions = Donation.objects.aggregate(total = Count('institution', distinct=True))

            return str(supported_institutions['total'])


        ctx = {
            'donation_count': get_total_donation_qty(),
            'supported_institutions': get_institution_count(),
            'foundations': Institution.objects.filter(type=1),
            'organisations': Institution.objects.filter(type=2),
            'fundraisings': Institution.objects.filter(type=3)
        }

        return render(request, 'index.html', ctx)


class AddDonation(View):

    @register.filter
    def get_value_in_qs(queryset, key):
        return queryset.values(key, flat=True)

    def get(self, request):

        if request.user.is_authenticated:

            categories = Category.objects.all()
            organisations = Institution.objects.all().order_by('name')
            ctx = {
                "categories": categories,
                "organisations": organisations
            }

            return render(request, 'form.html', context=ctx)

        else:

            return redirect('Login')


class Login(View):

    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):

        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('Homepage')
        else:
            return redirect(reverse('Register') + '#register')


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('Homepage')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            User.objects.create_user(first_name=name, last_name=surname, email=email, username = email, password = password)

            return redirect(reverse('Login') + '#login')
        
        return render(request, 'register.html')


@method_decorator(csrf_exempt, name='dispatch')
class AjaxFilter(View):
    """View for AJAX data exchange, request contains a list of chosen categories, response returns related Institution objects."""

    # TODO:: DESERIALIZE REQUEST, SERIALIZE RESPONSE
    def post(self, request):

        # Decode request body (bytestring --> string):
        reqbody = json.loads(request.body.decode())
        print('#####'*10)
        print(reqbody)
        print('#####'*10)

        # This is a list of chosen categories PKs (as strings):
        category_list = reqbody['serializedData']
        print('#####'*10)
        print(category_list, type(category_list))
        print('#####'*10)

        # This is the list of organisation PKs being sent along with the response:
        idList = list(set(Institution.objects.filter(categories__in=category_list).values_list('id', flat=True)))

        # There is no serializer, so just encode it.
        response = HttpResponse(json.dumps({"idList": idList}))

        return response
