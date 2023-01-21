import uuid , razorpay
from django.views.generic import  ListView
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from .models import  Categorys, CustomerCart, CustomerCheckout, Products, customerPayedProducts
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from storefront.forms import  CustomerCheckoutForm, LoginForm, RegistrationForm
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

def search(request):
    results = []
    if request.method == "GET":
        query = request.GET.get('search')
        if query == '':
            query = 'None'
        results = Products.objects.filter(Q(name__icontains=query) | Q(img__icontains=query) | Q(price__icontains=query))
    return render(request, 'storefront/search_page.html', {'query': query, 'results': results})


@login_required(login_url = reverse_lazy('login'))
def logout(request):
    auth.logout(request)
    return redirect("/")

def homepage(request):
    categories = Categorys.objects.all()
    return render(request,'homepage.html',{'categories': categories})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        
def register(request):
    if request.method == 'POST':
        registerform = RegistrationForm(request.POST)

        if registerform.is_valid():
            username = registerform.cleaned_data['username']
            email = registerform.cleaned_data['email']
            password = registerform.cleaned_data['password']
            cpassword = registerform.cleaned_data['cpassword']
             
            if User.objects.filter(email = email ).exists():
                registerform = RegistrationForm(request.POST)
                messages.info(request,'email taken')
                return render(request,'create-account.html',{'registerform':registerform})
            elif password != cpassword:
                registerform = RegistrationForm(request.POST)
                messages.info(request,'re-enter your password')
                return render(request,'create-account.html',{'registerform':registerform})    
            else:
                user = User.objects.create_user(username = username,email = email,password = password)
                user.save()
                return HttpResponseRedirect(reverse('login'))
            
        else:
            registerform = RegistrationForm(request.POST)
            context = {'registerform':registerform}
            return render(request, 'create-account.html',context)
    else:
        registerform = RegistrationForm()
    return render(request,'create-account.html',{'registerform':registerform})


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('homepage'))
    else:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                
                user = authenticate(username=username,password=password)
                if user is not None:
                    if user.is_active:
                        auth.login(request,user)  
                        return HttpResponseRedirect(reverse('homepage'))
                    else:
                        login_form = LoginForm(request.POST)
                        messages.info(request,'Invalid credentials')
                        return render(request,"login.html",{"form":login_form})
                else:
                    login_form = LoginForm(request.POST)
                    
                    return HttpResponseRedirect(reverse('homepage'))
            else:
                login_form = LoginForm(request.POST)
                messages.info(request,'Invalid credentials')
                return render(request,"login.html",{"form":login_form}) 
        else:
            login_form = LoginForm()
            return render(request,"login.html",{"form":login_form})
    

def viewMore(request,category_id):
    prod = Products.objects.filter(category = category_id)
    usercart = []
    return render(request,'view_more.html',{'prod': prod})

def guestaddtocart(request):
    return render(request,'guestcart.html')

def guestcheckoutcustomer(request):
    return render(request,'storefront/guestcheckout.html')

def guestcart(request):
    return render(request,'guestcart.html')

def detailpage(request,id):
    prod = Products.objects.get(id = id) 
    if request.user.is_authenticated:  
        usercart = CustomerCart.objects.filter(customer = request.user)
        cart_product_ids = []
        if usercart:
            for item in usercart:
                cart_product_ids.append(item.product.id)

        return render(request,'storefront/products_detail.html',{'prod': prod,'usercart':usercart, 'cart_product_ids': cart_product_ids})
    else:
        return render(request,'storefront/products_detail.html',{'prod': prod})    

@csrf_exempt
@login_required(login_url = reverse_lazy('login'))
def buynow(request):
    if is_ajax(request=request):
        product_id = int(request.POST['product'])
        message = request.POST['message']
        upgrade = request.POST['upgrade']
        content = request.POST['content']
        user = request.user
        usercart = CustomerCart.objects.filter(customer = request.user)
        cart_instance = CustomerCart(customer = user,product_id=product_id,message=message,upgrade=upgrade,content=content)
        if usercart:
            for item in usercart:
                if item == cart_instance:
                    return JsonResponse({'result':'failed'})
        else:

            cart_instance.save()
            print(usercart)
            return JsonResponse({'result':'success'})

@csrf_exempt
@login_required(login_url = reverse_lazy('login'))
def addtocart(request):
    if is_ajax(request=request):
        product_id = int(request.POST['product'])
        message = request.POST['message']
        upgrade = request.POST['upgrade']
        content = request.POST['content']
        user = request.user
        if CustomerCart.objects.filter(customer = user,product_id=product_id):
            return JsonResponse({'result':'failed'})
        else:
            cart_instance = CustomerCart(customer = user,product_id=product_id,message=message,upgrade=upgrade,content=content)
            cart_instance.save()
            return JsonResponse({'result':'success'})

@csrf_exempt
@login_required(login_url = reverse_lazy('login'))
def removefromcart(request):
     if is_ajax(request=request):
        product_id = int(request.POST['product'])
        user = request.user
        cart_instance = CustomerCart.objects.filter(customer = user,product_id=product_id)
        cart_instance.delete()
        return JsonResponse({'result':'success'})

@login_required(login_url = reverse_lazy('login'))
def removefromcartpage(request,product_id):
    user = request.user
    cart_instance = CustomerCart.objects.filter(customer = user,product=product_id)
    cart_instance.delete()
    return HttpResponseRedirect(reverse('usercart'))

@login_required(login_url = reverse_lazy('login'))                                      
def viewcustomercart(request):
    usercart = CustomerCart.objects.filter(customer = request.user).select_related('product')
    totalprice = sum(item.product.price for item in usercart)
    checkoutForm = CustomerCheckoutForm()
    return render(request,'customercart.html',{'usercart':usercart,
                                                        'totalprice':totalprice,
                                                        'checkoutform':checkoutForm})    

@login_required
def checkoutcustomer(request):
    if request.method == 'POST':
        user = request.user
        address = request.POST['address']
        phone = request.POST['phone']
        pincode = request.POST['pincode']
        date = request.POST['date']
        usercart = CustomerCart.objects.filter(customer = request.user).select_related('product')
        totalprice = sum(item.product.price for item in usercart)
        receipt = str(uuid.uuid1())
        client = razorpay.Client(auth=("rzp_test_NjFTSrtk8dCDt7", "vJjpGBMlQlJ0O0of5Rm7BlP5"))
        DATA = {
            'amount':totalprice*100,
            'currency':'INR',
            'receipt':'pydoracake',
            'payment_capture':1,
            'notes':{}
        }
        order_details = client.order.create(data=DATA)
        # return HttpResponse(order_details)
        customercheckout_order_instance = CustomerCheckout(customer = request.user,
                                            order_id = order_details.get('id'),
                                            total_amount = totalprice,
                                            reciept_num = receipt,
                                            delivery_address = address,
                                            delivery_phone = phone,
                                            pincode = pincode,
                                            date = date)
        customercheckout_order_instance.save()
        customercheckout = CustomerCheckout.objects.get(id = customercheckout_order_instance.id)
        for item in usercart:
            orderedproduct_instance = customerPayedProducts(customer = request.user,
                                                            product_name = item.product.name,
                                                            price = item.product.price,
                                                            checkout_details = customercheckout)
            orderedproduct_instance.save()
                                                            
        context = {'order_id' : order_details.get('id'),
                    'amount' : totalprice,
                    'amountscript' : totalprice*100,
                    'currency' : 'INR',
                    'companyname' : 'PyDoraCake',
                    'username' : request.user.first_name+' '+request.user.last_name,
                    'useremail' : request.user.email,
                    'phonenum' : phone,
                    'rzpkey' : 'rzp_test_bAYqeZhjXN8pf0'
                    }
        return render(request,'cheackoutform.html',context)
    else:
      return HttpResponseRedirect(reverse('usercart'))  

@csrf_exempt
@login_required(login_url = reverse_lazy('login'))
def markpaymentsuccess(request):
    if request.is_ajax():
        order_id = request.POST['order_id']
        payment_id = request.POST['payment_id']
        payment_signature = request.POST['payment_signature']
        user = request.user
        customercart_order_instance = CustomerCheckout.objects.get(order_id = order_id,
                                                                customer=user)
        customercart_order_instance.payment_signature = payment_signature
        customercart_order_instance.payment_id = payment_id
        customercart_order_instance.payment_complete = 1
        customercart_order_instance.save()
        customercart_instance = CustomerCart.objects.filter(customer = user)
        customercart_instance.delete()
        return JsonResponse({'result':'success'})        
             
   
    