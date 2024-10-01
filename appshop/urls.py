from django.urls import path
from appshop.views import Home, CartPage, Detail, Checkout, Shop, ContactPage, logindef, Logout, CategoryPage, add_to_cart, CommentPage, profile, upload_profile_picture, remove_profile_picture, update_cart, DressPage, search, AdminPage, delete_order, delete_all_orders

urlpatterns = [
    path('', Home, name='home'),
    path('cart/', CartPage, name='cart'),
    path('product/<slug:slug>/', Detail, name='detail'),
    path('checkout/', Checkout, name='checkout'),
    path('shop/', Shop, name='shop'),
    path('contact/', ContactPage, name='contact'),
    path('login/', logindef, name='login'),
    path('logout/', Logout, name='logout'),
    path('category/<slug:slug>/', CategoryPage, name='category'),
    path('profile/', profile, name='profile'),
    path('remove-profile-picture/', remove_profile_picture, name='remove_profile_picture'),
    path('comment/', CommentPage, name='comment'),
    path('addtocart/<int:id>/', add_to_cart, name='addtocart'),
    path('update-cart/', update_cart, name='update_cart'),
    path('upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
    path('remove-profile-picture/', remove_profile_picture, name='remove_profile_picture'),
    path('dress/<str:gender>/', DressPage, name='dress'),
    path('search/', search, name='search'),
    path('adminpage/', AdminPage, name='adminpage'),
    path('adminpage/delete/<int:order_id>/', delete_order, name='delete_order'),
    path('adminpage/delete_all/', delete_all_orders, name='delete_all_orders'),

]