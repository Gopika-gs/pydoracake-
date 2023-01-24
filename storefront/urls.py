from django.urls import  path
from . import views
from .views import DetailView


urlpatterns=[
    path('',views.homepage, name='homepage'),
    path("search/", views.search, name="search"),
    path('register/', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login'),
    path('viewMore/<int:category_id>/', views.viewMore, name='viewMore'),
    path('detailpage/<id>', views.detailpage, name='detailpage'),
    path('addtocart', views.addtocart, name='addtocart'),
    path('usercart', views.viewcustomercart, name='usercart'),
    path('removefromcart', views.removefromcart, name='removefromcart'),
    path('removefromcartpage/<int:product_id>', views.removefromcartpage, name='removefromcartpage'),
    path('guestcart', views.guestcart, name='guestcart'),
    path('checkoutcustomer', views.checkoutcustomer, name='checkoutcustomer'),
    path('markpaymentsuccess', views.markpaymentsuccess, name='markpaymentsuccess'),
    path('guestaddtocart', views.guestaddtocart, name='guestaddtocart'),
    path('guestcheckoutcustomer', views.guestcheckoutcustomer, name='guestcheckoutcustomer'),
    path('buynow', views.buynow, name='buynow'),
    path('paymentsuccess', views.paymentsuccess, name='paymentsuccess'),
    path('placeorder',views.placeorder, name='placeorder'),
     
]