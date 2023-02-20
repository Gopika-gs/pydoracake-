from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from storefront.views import is_ajax
from .models import Categorys, Products
from storefront.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def loginadmin(request):
    if request.user.is_authenticated:
        return  HttpResponseRedirect (reverse('admindashboard'))
        
    else:	
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                                
                if user is not None:
                    if user.is_active and user.is_superuser:
                        login(request,user)	
                        return HttpResponseRedirect(reverse('admindashboard'))
                    else:
                        return HttpResponse('Your account is not active')
                else:
                    return HttpResponse('The Account does not exists')
            else:
                login_form = LoginForm()
                return render(request, "login.html",{"form":login_form})
        else:
            login_form = LoginForm()
        return render(request,'login.html',{"form":login_form})
    


def checksuperuser(user):
    return user.is_superuser

@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def logoutadmin(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def admindashboard(request):
    return render(request,'admindashboard.html',{})

@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def addcategorys(request):
    category = Categorys.objects.all()
    return render(request,'addcategorys.html',{'category':category})

@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def addproducts(request):
    category = Categorys.objects.all()
    products = Categorys.objects.all()
    print(category,products)
    return render(request,'addproducts.html',{'products':products,'category':category})

@csrf_exempt
@login_required(login_url = reverse_lazy('login'))
def addingcategory(request):
    if is_ajax(request=request):
        name = request.POST['name']
        image = request.POST['img']
        category = Categorys.objects.filter(name = name)
        if category:
            for item in category:
                if item == category_instance:
                    return JsonResponse({'result':'failed'})
        else:
            category_instance = Categorys(img = image,
                                        name = name) 
            category_instance.save()
            return JsonResponse({'result':'success'})
          
@csrf_exempt
@login_required(login_url = reverse_lazy('login'))
def addingproduct(request):
    if is_ajax(request=request):
        name = request.POST['name']
        image = request.POST['img']
        price = request.POST['price']
        category = request.POST['category']
        flavour = request.POST['flavour']
        size = request.POST['size']
        shape = request.POST['shape']
        products = Products.objects.filter(name = name)
        if products:
            for item in products:
                if item == products:
                    return JsonResponse({'result':'failed'})
        else:
            product_instance = Products(name = name,
                                            img = image,
                                            category = category,
                                            flavour = flavour,
                                            price = price,
                                            shape = shape,
                                            size = size,) 
            product_instance.save()
            return JsonResponse({'result':'success'})

def viewproducts(request):
    products = Products.objects.all()
    category = Categorys.objects.all()
    return render(request,'viewproduct.html',{'products':products,'category':category})
