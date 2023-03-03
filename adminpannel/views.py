import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from storefront.models import Order
from storefront.views import is_ajax
from .models import Categorys, Products
from storefront.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from datetime import date
import csv
from django.contrib.auth.models import User,auth

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
                        return HttpResponseRedirect(reverse('dashboard'))
                    else:
                        return HttpResponse('Your account is not active')
                else:
                    return HttpResponse('The Account does not exists')
            else:
                login_form = LoginForm()
                return render(request, "login.html",{"form":login_form})
        else:
            login_form = LoginForm()
            messages.success(request,"Logined successfully")
        return render(request,'login.html',{"form":login_form})
    
@login_required(login_url = reverse_lazy('login'))
def logout(request):
    auth.logout(request)
    return redirect("/")

def checksuperuser(user):
    return user.is_superuser

@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def logoutadmin(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@csrf_exempt
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def admindashboard(request):
    orders_c = Order.objects.filter(status='Ordered')
    process_c = Order.objects.filter(status='Processing')
    dispatch_c = Order.objects.filter(status='Dispatched')
    deliver_c = Order.objects.filter(status='Delivered')
    order_count = len(orders_c)
    processing_count = len(process_c)
    dispatched_count = len(dispatch_c)
    delivered_count = len(deliver_c)
    return render(request,'admindashboard.html',{'order_count':order_count,
                                                 'processing_count':processing_count,
                                                 'dispatched_count':dispatched_count,
                                                 'delivered_count' :delivered_count})

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
        image = request.FILES['img']
        category = Categorys.objects.filter(name = name)
        category_instance = Categorys(img = image,
                                        name = name) 
        if Categorys.objects.filter(name=name):
            messages.warning(request, 'Adding category failed.')
            return JsonResponse({'result':'failed'})

        else:
            category_instance = Categorys(img = image,
                                        name = name) 
            category_instance.save()
            messages.success(request, 'Category added.')
            return JsonResponse({'result':'success'})
          
@csrf_exempt
@login_required(login_url = reverse_lazy('login'))
def addingproduct(request):
    if is_ajax(request=request):
        name = request.POST['name']
        image = request.FILES['img']
        price = request.POST['price']
        category = request.POST['category']
        flavour = request.POST['flavour']
        size = request.POST['size']
        shape = request.POST['shape']
        products = Products.objects.filter(name = name)
        prod_instance = Categorys.objects.get(id =category)
        if Products.objects.filter(name=name):
            messages.warning(request, 'Adding product failed.')
            return JsonResponse({'result':'failed'})
        else:
            product_instance = Products(name = name,
                                            img = image,
                                            category = prod_instance,
                                            flavour = flavour,
                                            price = price,
                                            shape = shape,
                                            size = size,) 
            product_instance.save()
            messages.success(request, 'Product added.')
            return JsonResponse({'result':'success'})

def viewproducts(request):
    products = Products.objects.all()
    category = Categorys.objects.all()
    return render(request,'viewproduct.html',{'products':products,'category':category})

def viewcategory(request):
    category = Categorys.objects.all()
    return render(request,'viewcategory.html',{'category':category})

def removeproduct(request,id):
    products = Products.objects.filter(id=id)
    products.delete()
    return HttpResponseRedirect(reverse('viewproducts'))

def editproduct(request,id):
    product = Products.objects.filter(id=id)
    category = Categorys.objects.all()
    return render(request,'editproduct.html',{'product':product,'category':category})

def removecategory(request,id):
    category = Categorys.objects.filter(id=id)
    category.delete()
    return HttpResponseRedirect(reverse('viewcategory'))

def editcategory(request,id):
    category = Categorys.objects.filter(id=id)
    return render(request,'editcategory.html',{'category':category})

@csrf_exempt
def savingedit(request):
    print("hello")
    if is_ajax(request=request):
        id = request.POST.get('product_id')
        name = request.POST['name']
        if request.FILES:
            image = request.FILES['img']
        else:
            print("no image is uploaded")
            print(id)
        price = request.POST['price']
        category = request.POST['category']
        flavour = request.POST['flavour']
        size = request.POST['size']
        shape = request.POST['shape']
        prod_instance = Categorys.objects.get(id = category)
        edit = Products.objects.filter(id=id).update(name = name,
                                            img =image,
                                            category = prod_instance,
                                            flavour = flavour,
                                            price = price,
                                            shape = shape,
                                            size = size,)
        messages.success(request, 'Product edited successfully.')
        return JsonResponse({'result':'success'})
    
@csrf_exempt
def savingcatedit(request):
    if is_ajax(request=request):
        id = request.POST.get('category_id')
        name = request.POST['name']
        if request.FILES:
            image = request.FILES['img']
        else:
            print("no image is uploaded")
            print(id)
    edit = Categorys.objects.filter(id=id).update(name = name,
                                                img = image,)
    messages.success(request, 'category edited successfully.')
    return JsonResponse({'result':'success'})
        
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def viewuser(request):
    users = User.objects.filter(is_superuser = 0,is_staff = 0)
    return render(request,'viewuser.html',{'users':users})

def userdetail(request,user_id):
    user = User.objects.filter(id=user_id)
    orders = Order.objects.filter(customer = user_id)
    return render(request,'userview.html',{'user':user,'orders':orders})

@csrf_exempt
def deleteuser(request):
    if is_ajax(request=request):
        id = request.POST['user_id']
        user = User.objects.filter(id=id)
        user.delete()
        return JsonResponse({'result':'success'})

@csrf_exempt
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def changestatususer(request):
    if request.method == 'POST':
        action = request.POST['action']
        user_id = int(request.POST['user_id'])
        user_instance = User.objects.get(id=user_id)
        if action == "disable":
            user_instance.is_active = 0
        else:
            user_instance.is_active = 1
        user_instance.save()
        return JsonResponse({'result':'success'})
    
@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def todayssalesreport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="salesreport"'+str(date.today())+'".csv"'
    writer = csv.writer(response)
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    sales = Order.objects.filter(payedon__range=(today_min, today_max))
    writer.writerow(['Order_id', 'Payment_id', 'Amount', 'Reciept', 'Phonenum', 'Address'])
    for sale in sales:
        writer.writerow([sale.order_id, sale.payment_id, sale.total_amount, sale.reciept_num, sale.delivery_phone, sale.delivery_address])
    return response

@user_passes_test(checksuperuser,login_url = reverse_lazy('login'))
def adminviewreports(request):
    return render(request,'salesreport.html',{})

def vieworder(request,stat):
    if request.method == 'GET':
        
        status = request.GET.get('status')
        if status =='Processing' or stat == 'Processing':
            orders = Order.objects.filter(status='Processing')
        elif status =='Ordered' or stat == 'Ordered':
            orders = Order.objects.filter(status='Ordered')
        elif status =='Delivered' or stat == 'Delivered':
            orders = Order.objects.filter(status='Delivered')
        elif status =='Dispatched' or stat == 'Dispatched':
            orders = Order.objects.filter(status='Dispatched')
        elif status =='none' or stat == 'none':
            orders = Order.objects.all()
        else :
            orders = Order.objects.all()

    return render(request,'vieworder.html',{'orders':orders})

@csrf_exempt
def process(request):
    if is_ajax(request=request):
        id = request.POST['order_id']
        order = Order.objects.filter(id=id).update(status='Processing')
        return JsonResponse({'result':'success'})

@csrf_exempt  
def dispatch(request):
    if is_ajax(request=request):
        id = request.POST['order_id']
        order = Order.objects.filter(id=id).update(status='Dispatched')
        return JsonResponse({'result':'success'})

@csrf_exempt   
def deliver(request):
    if is_ajax(request=request):
        id = request.POST['order_id']
        order = Order.objects.filter(id=id).update(status='Delivered')
        return JsonResponse({'result':'success'})
    