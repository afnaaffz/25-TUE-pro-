from django.urls import path

from new_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("indexx", views.indexx, name="indexx"),
    path("login_page", views.login_page, name="login_page"),
    path('logout/', views.logout_page, name='logout_page'),

    path("customer_register", views.customer_register, name="customer_register"),
    path("customers", views.customers, name="customers"),


    path("dashboard", views.dashboard, name="dashboard"),

    path("about", views.about, name="about"),
    path("carts", views.carts, name="carts"),
    path('delete_item/<int:cart_id>/<int:cart_item_id>/', views.delete_item, name='delete_item'),

    path("order", views.order, name="order"),
    path("my_orders", views.my_orders, name="my_orders"),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),

    path("contact", views.contact, name="contact"),
    path('contact_success/', views.contact_success, name='contact_success'),

    path('product_single/<int:product_id>/', views.product_single, name='product_single'),

    path("shop", views.shop, name="shop"),
    path("success", views.success, name="success"),

    path("customer_address_add", views.customer_address_add, name="customer_address_add"),
    path("customer_address_view", views.customer_address_view, name="customer_address_view"),
    path('customer_address_delete/<int:customer_address_id>/', views.customer_address_delete, name='customer_address_delete'),
    path('customer_address_edit/<int:customer_address_id>/', views.customer_address_edit, name='customer_address_edit'),

    path("category_add", views.category_add, name="category_add"),
    path("category_view", views.category_view, name="category_view"),
    path("category_delete/<int:category_id>/", views.category_delete, name="category_delete"),
    path("category_edit/<int:category_id>/", views.category_edit, name="category_edit"),

    path("subcategory_add", views.subcategory_add, name="subcategory_add"),
    path("subcategory_view", views.subcategory_view, name="subcategory_view"),
    path("subcategory_delete/<int:subcategory_id>/", views.subcategory_delete, name="subcategory_delete"),
    path("subcategory_edit/<int:subcategory_id>/", views.subcategory_edit, name="subcategory_edit"),

    path("brand_add", views.brand_add, name="brand_add"),
    path("brand_view", views.brand_view, name="brand_view"),
    path('brand_edit/<int:brand_id>/', views.brand_edit, name='brand_edit'),
    path('brand_delete/<int:brand_id>/', views.brand_delete, name='brand_delete'),

    path("product_add", views.product_add, name="product_add"),
    path("product_view", views.product_view, name="product_view"),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('product_edit/<int:product_id>/', views.product_edit, name='product_edit'),

    path("order_view", views.order_view, name="order_view"),
    path('order_edit/<int:order_id>/', views.order_edit, name='order_edit'),

    path("customer_sales_report", views.customer_sales_report, name="customer_sales_report"),
    path("product_sales_report", views.product_sales_report, name="product_sales_report"),
    path("brand_sales_report", views.brand_sales_report, name="brand_sales_report"),
    path("category_sales_report", views.category_sales_report, name="category_sales_report"),

    path("banner_add", views.banner_add, name="banner_add"),
    path("banner_view", views.banner_view, name="banner_view"),

    path("variant_add", views.variant_add, name="variant_add"),
    path("variant_view", views.variant_view, name="variant_view"),
    path('add_values/<int:variant_id>/', views.add_values, name='add_values'),
    path('variant_details/<int:variant_id>/', views.variant_details, name='variant_details'),

]
