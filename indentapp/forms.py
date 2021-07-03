from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Indent

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),

)
DEPT_CHOICES = (
    ("IT", "IT"),
    ("Account", "Account"),

)


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    dept = forms.ChoiceField(choices=DEPT_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'birth_date', 'gender', 'dept', 'password1', 'password2',)


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_category", "product_name"]  # use = '__all__'


class ProductVoucherForm(forms.ModelForm):
    requested_amount = forms.FloatField(required=False)
    paid_amount = forms.FloatField(required=False)
    balance = forms.FloatField(required=False)

    class Meta:
        model = Indent
        fields = ['user', 'category', 'product', 'product_price', 'product_quantity', 'requested_amount', 'paid_amount',
                  'balance']
