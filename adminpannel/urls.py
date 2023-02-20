from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
     path('adminlogin', views.loginadmin, name='adminlogin'),
     path('', RedirectView.as_view(url='adminlogin')),
     path('adminlogout', views.logoutadmin, name='adminlogout'),
     path('dashboard', views.admindashboard, name='admindashboard'),
     path('addcategorys', views.addcategorys, name='addcategorys'),
     path('addproducts', views.addproducts, name='addproducts'),
     path('addingcategory', views.addingcategory, name='addingcategory'),
     path('addingproduct', views.addingproduct, name='addingproduct'),
     path('viewproducts', views.viewproducts, name='viewproducts')
     
     ]