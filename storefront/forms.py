from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control username','placeholder':'Username'}),required = True)
    email = forms.CharField(widget = forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),required = True)
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),required = True)
    cpassword = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}),required = True)

class LoginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),required = True)
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),required = True)
   
class CustomerCheckoutForm(forms.Form):
    phone = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control','placeholder':'Mobile number'}),max_length= 200, required=True)
    address = forms.CharField(widget = forms.Textarea(attrs={'class':'form-control','placeholder':'Delivery address',"rows":5}),max_length= 2000, required=True)