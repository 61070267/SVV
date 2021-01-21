from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm

from .models import ShopOwner, Customer, Payment

# UserCreationForm + bootstrap class 
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model=User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(user,*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(user,*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class ShopOwnerForm(forms.ModelForm):
    class Meta:
        model = ShopOwner
        exclude = ('username',)
        labels = {
            'shop_desc': "Description",
            'shop_icon': "Icon",
            'shop_bg': "Background",
        }
        widgets = {
            'shop_desc': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['shop_name'].widget.attrs['class'] = 'form-control'
        self.fields['shop_address'].widget.attrs['class'] = 'form-control'
        self.fields['shop_desc'].widget.attrs['class'] = 'form-control'
        self.fields['shop_icon'].widget.attrs['class'] = 'form-control'
        self.fields['shop_bg'].widget.attrs['class'] = 'form-control'

        self.fields['shop_icon'].widget.attrs['onchange'] = 'showImg(this)'
        self.fields['shop_bg'].widget.attrs['onchange'] = 'showImg(this, 800, 450)'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ('username',)
        labels = {
            'cus_fname': "First Name",
            'cus_lname': "Last Name",
            'cus_address': "Address",
            'cus_img': "Image"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['cus_fname'].widget.attrs['class'] = 'form-control'
        self.fields['cus_lname'].widget.attrs['class'] = 'form-control'
        self.fields['cus_address'].widget.attrs['class'] = 'form-control'
        self.fields['cus_img'].widget.attrs['class'] = 'form-control'

        self.fields['cus_img'].widget.attrs['onchange'] = 'showImg(this)'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ('cart_id', 'amount')
        labels = {
            'payment': "Pay by",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['payment'].widget.attrs['class'] = 'form-control'
        #self.fields['payment'].widget.attrs['onchange'] = 'showImg(this)'