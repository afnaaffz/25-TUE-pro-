from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator, MaxLengthValidator
from new_app.models import CustomerAddress, Category, Subcategory, Brand,  Products, Login, \
    Register, Cart, Contact, CartItem, Order, OrderItem, Banner, Variant, VariantValue, VariantAdd


class Login_Form(UserCreationForm):
    class Meta:
        model = Login
        fields = ("username","password1","password2")

class Register_Form(forms.ModelForm):
    class Meta:
        model = Register
        fields =('__all__')
        exclude = ('user',)


class CustomerAddressForm(forms.ModelForm):
    pincode = forms.CharField(max_length=6, validators=[MinLengthValidator(6), MaxLengthValidator(6)])
    phone_no = forms.CharField(max_length=10, validators=[MinLengthValidator(10), MaxLengthValidator(10)])


    class Meta:
        model = CustomerAddress
        fields = ['customer', 'address', 'pincode', 'phone_no']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'status']



class SubcategoryForm(forms.ModelForm):

    class Meta:
        model = Subcategory
        fields = '__all__'


class BrandForm(forms.ModelForm):

    class Meta:
        model = Brand
        fields = '__all__'




class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['product_name', 'category', 'subcategory', 'brand', 'description', 'status', 'primary_variant', 'secondary_variant', 'image']



class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'


class VariantAddForm(forms.ModelForm):
    class Meta:
        model = VariantAdd
        fields = '__all__'

class VariantValueForm(forms.ModelForm):
    class Meta:
        model = VariantValue
        fields = '__all__'

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'

