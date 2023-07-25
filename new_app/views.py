from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from new_app.forms import CustomerAddressForm, SubcategoryForm, BrandForm, \
    CategoryForm, Login_Form, Register_Form, CartForm, ContactForm, OrderForm, OrderItemForm, BannerForm, VariantForm, VariantValueForm, ProductsForm
from new_app.models import CustomerAddress, Category, Subcategory, Brand, Login, \
    Register, Cart, Contact, CartItem, Order, OrderItem, Banner, Variant, VariantValue,Products


# Create your views here.


def index(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product_id)
            product = get_object_or_404(Products, id=product_id, status=1)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] = quantity - 1
                else:
                    if quantity < product.product_stock:  # Change 'quantity' to 'product_stock'
                        cart[product_id] = quantity + 1
            else:
                cart[product_id] = 1
        else:
            cart = {}
            cart[product_id] = 1

        request.session['cart'] = cart
        return redirect('index')

    all_products = Products.objects.filter(status=1)
    first_section_products = all_products.order_by('-id')[:4]
    second_section_products = all_products[4:8]
    active_banners = Banner.objects.filter(status=1)

    context = {
        'first_section_products': first_section_products,
        'second_section_products': second_section_products,
        'active_banners': active_banners,
    }

    return render(request, "index.html", context)


@login_required
def indexx(request):
    return render(request,"indexx.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pass")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_customer:
                return redirect("index")
        else:
            return render(request, "login.html", {"error_message": "Customer has not been registered"})
    return render(request, "login.html")


def customer_register(request):
    form1 = Login_Form()
    form1 = Login_Form()
    form2 = Register_Form()
    if request.method == "POST":
        form1 = Login_Form(request.POST)
        form2 = Register_Form(request.POST)

        if form1.is_valid() and form2.is_valid():
            a = form1.save(commit=False)
            a.is_customer = True
            a.save()
            user1 = form2.save(commit=False)
            user1.user = a
            user1.save()
            return redirect("login_page")
    return render(request,"register.html", {'form1':form1, 'form2':form2})


@login_required
def customers(request):
    return render(request,"customer/customers.html")



def dashboard(request):
    return render(request,"dashboard.html")

def about(request):
    return render(request,"about.html")


def logout_page(request):
    if request.user.is_authenticated:
        cart = request.session.get('cart', {})
        user_cart = cart.get(str(request.user.id))
        if user_cart:
            cart[str(request.user.id)] = user_cart
            del cart[str(request.user.id)]
            request.session['cart'] = cart
    logout(request)
    return redirect('index')



def carts(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        cart = Cart.objects.get_or_create(customer=request.user)[0]
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        if not created:
            cart_item.quantity += 1
        cart_item.price = cart_item.product.selling_price  # Change 'price' to 'selling_price'
        cart_item.total_price = cart_item.quantity * cart_item.price
        cart_item.save()
        cart.total += cart_item.total_price
        cart.save()
        return redirect('carts')

    cart = Cart.objects.filter(customer=request.user).prefetch_related('cart_items').first()  # Retrieve the first cart object
    if cart:
        cart_items = cart.cart_items.all()
        total = sum(item.total_price for item in cart_items)
    else:
        cart_items = []
        total = 0

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'carts.html', context)



def delete_item(request, cart_id, cart_item_id):
    cart = get_object_or_404(Cart, id=cart_id, customer=request.user)
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)

    cart.total -= cart_item.total_price
    cart.save()
    cart_item.delete()

    return redirect("carts")





def order(request):
    user = request.user

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        district = request.POST.get('district')

        cart = Cart.objects.filter(customer=user).prefetch_related('cart_items').first()
        if cart:
            cart_items = cart.cart_items.all()

            total = sum(item.total_price for item in cart_items)

            order = Order.objects.create(
                customer=user,
                created_by=user,
                total=total,
                address=address,
                phone=phone,
                district=district,
                status='ordered'
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.total_price
                )
                # Decrease the quantity of the product in product_view
                Products.objects.filter(id=item.product.id).update(quantity=F('quantity') - item.quantity)

            cart.delete()

            return redirect("success")

    else:
        form = OrderItemForm()

    cart = Cart.objects.filter(customer=user).prefetch_related('cart_items').first()
    if cart:
        cart_items = cart.cart_items.all()
        cart_total = sum(item.total_price for item in cart_items)
    else:
        cart_items = []
        cart_total = 0

    context = {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'user': user,
        'customer_name': user.username if user.is_authenticated else "",
    }
    return render(request, "order.html", context)

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, "my_orders.html", {'orders': orders})

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    cart_items = OrderItem.objects.filter(order=order)
    return render(request, "order_details.html", {'order': order, 'cart_items': cart_items})




@login_required
def success(request):
    user = request.user
    try:
        order = Order.objects.filter(customer=user).latest('id')
    except Order.DoesNotExist:
        order = None

    return render(request, "success.html", {'order': order})


def contact(request):
        form = ContactForm()
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                contact = form.save()
                return redirect("contact_success")
        return render(request, 'contact.html', {'form': form})


def contact_success(request):
    contact = Contact.objects.all()
    return render(request, "contact_success.html", {'contact': contact})


def product_single(request, product_id):
    products = Products.objects.all()
    product = get_object_or_404(Products, id=product_id)
    out_of_stock = product.product_stock < 1  # Change 'quantity' to 'product_stock'

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if out_of_stock:
            return render(request, 'product_single.html', {'product': product, 'products': products, 'out_of_stock': out_of_stock})

        cart = Cart.objects.get_or_create(customer=request.user)[0]
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.price = product.selling_price  # Change 'price' to 'selling_price'
        cart_item.total_price = cart_item.quantity * cart_item.price
        cart_item.save()
        cart.total += cart_item.total_price
        cart.save()

        return redirect('carts')

    return render(request, 'product_single.html', {'product': product, 'products': products, 'out_of_stock': out_of_stock})



def shop(request):
    categories = Category.objects.filter(status=1)
    subcategories = Subcategory.objects.filter(status=1)
    products = Products.objects.filter(category__status=1, subcategory__status=1, brand__status=1)

    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        subcategory_id = request.POST.get('subcategory_id')

        if category_id == 'all' or subcategory_id == 'all':
            products = Products.objects.filter(category__status=1, subcategory__status=1, brand__status=1)
        else:
            try:
                category = Category.objects.get(id=category_id, status=1)
                subcategory = Subcategory.objects.get(id=subcategory_id, status=1)
                products = Products.objects.filter(subcategory=subcategory, subcategory__category=category, category__status=1, subcategory__status=1, brand__status=1)
            except (Category.DoesNotExist, Subcategory.DoesNotExist):
                products = Products.objects.none()

        # Handle adding to cart
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  # Rename 'quantity' to 'product_stock'

        try:
            product = Products.objects.get(id=product_id, category__status=1, subcategory__status=1, brand__status=1)
        except Products.DoesNotExist:
            pass
        else:
            cart = Cart.objects.get_or_create(customer=request.user)[0]
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            cart_item.total_price = product.selling_price * cart_item.quantity  # Use total_price field for the cart item's price
            cart_item.save()
            cart.total += cart_item.total_price
            cart.save()

            return redirect('carts')

    # Disable Add to Cart button for products with quantity less than 1
    for product in products:
        if product.product_stock < 1:  # Change 'quantity' to 'product_stock'
            product.disable_add_to_cart = True
        else:
            product.disable_add_to_cart = False

    return render(request, 'shop.html', {'products': products, 'categories': categories, 'subcategories': subcategories})


def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)



####CUSTOMER


def customer_address_add(request):
    customers = Register.objects.all()
    if request.method == 'POST':
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            customer_address = form.save()
            return redirect("customer_address_view")
    else:
        form = CustomerAddressForm()

    return render(request, 'customer_address/customer_address_add.html', {'form': form, 'customers': customers})


def customer_address_view(request):
    customer_address = CustomerAddress.objects.all()
    return render(request, 'customer_address/customer_address_view.html', {'customer_address': customer_address})


def customer_address_edit(request,customer_address_id):
    a = CustomerAddress.objects.get(id=customer_address_id)
    form = CustomerAddressForm(instance=a)
    if request.method == 'POST':
        form = CustomerAddressForm(request.POST,instance=a)
        if form.is_valid():
            customer_address = form.save(commit=False)
            customer_address.status = 1
            customer_address.save()
            return redirect("customer_address_view")
    return render(request, "customer_address/customer_address_edit.html", {'form': form})

def customer_address_delete(request, customer_address_id):
    try:
        customer_address = CustomerAddress.objects.get(id=customer_address_id)
        customer_address.delete()
        return redirect("customer_address_view")
    except CustomerAddress.DoesNotExist:
        return HttpResponse("The customer address does not exist.")


#####CATEGORY


def category_add(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect("category_view")
    return render(request, 'category/category_add.html', {'form': form})


def category_view(request):
    categories = Category.objects.all()
    return render(request, 'category/category_view.html', {'categories': categories})


def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)
    form = CategoryForm(instance=category)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect("category_view")

    return render(request, "category/category_edit.html", {'form': form})



def category_delete(request,category_id):
    wm = Category.objects.get(id=category_id)
    wm.delete()
    return redirect("category_view", category_id=category_id)


########SUBCATEGORY


def subcategory_add(request):
    form = SubcategoryForm()
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save()
            return redirect("subcategory_view")
    return render(request, 'subcategory/subcategory_add.html', {'form': form})


def subcategory_view(request):
    subcategory = Subcategory.objects.all()
    return render(request, 'subcategory/subcategory_view.html', {'subcategory': subcategory})


def subcategory_edit(request, subcategory_id):
    subcategory = Subcategory.objects.get(id=subcategory_id)
    form = SubcategoryForm(instance=subcategory)

    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.save()
            return redirect("subcategory_view")

    return render(request, "subcategory/subcategory_edit.html", {'form': form})


def subcategory_delete(request,subcategory_id):
    wm = Subcategory.objects.get(id=subcategory_id)
    wm.delete()
    return redirect("subcategory_view")


######BRAND


def brand_add(request):
    form = BrandForm()
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            brand = form.save(commit=False)
            brand = form.save()
            return redirect("brand_view")
    return render(request, 'brand/brand_add.html', {'form': form})


def brand_view(request):
    brand = Brand.objects.all()
    return render(request, 'brand/brand_view.html', {'brand': brand})


def brand_edit(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)

    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('brand_view')
    else:
        form = BrandForm(instance=brand)

    return render(request, 'brand/brand_edit.html', {'form': form})


def brand_delete(request, brand_id):
    wm = Brand.objects.get(id=brand_id)
    wm.delete()
    return redirect("brand_view")


#########PRODUCT



def product_add(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect("product_view")

    else:
        form = ProductsForm()

    return render(request, 'product/product_add.html', {'form': form})

def product_view(request):
    products = Products.objects.all()
    return render(request, 'product/product_view.html', {'products': products})




def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)




def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductsForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_view')
    else:
        form = ProductsForm(instance=product)

    return render(request, 'product/product_edit.html', {'form': form})



######ORDER

def order_view(request):
    orders = Order.objects.all()
    return render(request, 'order/order_view.html', {'orders': orders})

def order_edit(request, order_id):
    order = Order.objects.get(id=order_id)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect("order_view")

    return render(request, "order/order_edit.html", {'form': form})



#####SALES REPORT


def customer_sales_report(request):
    customers = Login.objects.filter(is_customer=True)

    report_data = []
    for customer in customers:
        register = Register.objects.get(user=customer)
        total_quantity = OrderItem.objects.filter(order__customer=customer).aggregate(total_quantity=Sum('quantity'))
        total_amount = OrderItem.objects.filter(order__customer=customer).aggregate(total_amount=Sum('price'))
        if total_quantity['total_quantity'] is not None and total_amount['total_amount'] is not None:
            report_data.append({
                'id': customer.id,
                'customer_name': register.name,
                'quantity_sold': total_quantity['total_quantity'],
                'amount': total_amount['total_amount']
            })

    return render(request, 'report/customer_sales_report.html', {'report_data': report_data})


def product_sales_report(request):
    products = Products.objects.all()

    report_data = []
    for product in products:
        total_quantity_sold = OrderItem.objects.filter(product=product).aggregate(total_quantity=Sum('quantity'))
        total_amount_sold = OrderItem.objects.filter(product=product).aggregate(total_amount=Sum('price'))
        if total_quantity_sold['total_quantity'] is not None and total_amount_sold['total_amount'] is not None:
            updated_product = Products.objects.get(id=product.id)
            report_data.append({
                'id': product.id,
                'product_name': updated_product.product_name,
                'quantity_sold': total_quantity_sold['total_quantity'],
                'amount': total_amount_sold['total_amount']
            })
    return render(request, 'report/product_sales_report.html', {'report_data': report_data})


def brand_sales_report(request):
    brands = Brand.objects.all()

    report_data = []
    for brand in brands:
        total_quantity_sold = OrderItem.objects.filter(product__brand=brand).aggregate(total_quantity=Sum('quantity'))
        total_amount_sold = OrderItem.objects.filter(product__brand=brand).aggregate(total_amount=Sum('price'))
        if total_quantity_sold['total_quantity'] is not None and total_amount_sold['total_amount'] is not None:
            updated_brand = Brand.objects.get(id=brand.id)
            report_data.append({
                'id': brand.id,
                'brand_name': updated_brand.name,
                'quantity_sold': total_quantity_sold['total_quantity'],
                'amount': total_amount_sold['total_amount']
            })

    return render(request, 'report/brand_sales_report.html', {'report_data': report_data})

def category_sales_report(request):
    categories = Category.objects.all()

    report_data = []
    for category in categories:
        total_quantity_sold = OrderItem.objects.filter(product__category=category).aggregate(total_quantity=Sum('quantity'))
        total_amount_sold = OrderItem.objects.filter(product__category=category).aggregate(total_amount=Sum('price'))
        if total_quantity_sold['total_quantity'] is not None and total_amount_sold['total_amount'] is not None:
            updated_category = Category.objects.get(id=category.id)
            report_data.append({
                'id': category.id,
                'category_name': updated_category.name,
                'quantity_sold': total_quantity_sold['total_quantity'],
                'amount': total_amount_sold['total_amount']
            })

    return render(request, 'report/category_sales_report.html', {'report_data': report_data})



def banner_add(request):
    form = BannerForm()
    if request.method == 'POST':
        form = BannerForm(request.POST,request.FILES)
        if form.is_valid():
            banner = form.save(commit=False)
            banner = form.save()
            return redirect("banner_view")
    return render(request, 'banner/banner_add.html', {'form': form})

def banner_view(request):
    banners = Banner.objects.filter(status=True)
    return render(request, 'banner/banner_view.html', {'banners': banners})



def variant_add(request):
    form = VariantForm()
    if request.method == 'POST':
        form = VariantForm(request.POST)
        if form.is_valid():
            variant = form.save()
            return redirect('variant_view')  # Redirect to variant_view page
    return render(request, 'variant/variant_add.html', {'form': form})


def variant_view(request):
    variants = Variant.objects.all()
    return render(request, 'variant/variant_view.html', {'variants': variants})



from django.urls import reverse

def add_values(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)

    if request.method == 'POST':
        form = VariantValueForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            VariantValue.objects.create(variant=variant, value=value)
            return redirect(reverse('variant_details', args=[variant_id]))  # Redirect to variant_details view
    else:
        form = VariantValueForm()

    context = {
        'variant': variant,
        'form': form
    }
    return render(request, 'variant/add_values.html', context)





def variant_details(request, variant_id):
    variant = get_object_or_404(Variant, id=variant_id)

    context = {
        'variant': variant
    }
    return render(request, 'variant/variant_details.html', context)







