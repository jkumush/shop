from django.urls import path
from .views import ProductList, ProductCreate, ProductListCreate, ProductDelete, ProductDetail, CategoryList, CommentList, ContactList

urlpatterns = [
    path('products/', ProductList.as_view(), name='products'),
    path('create/', ProductCreate.as_view(), name='product-create'),
    path('list-create/', ProductListCreate.as_view(), name='product-list-create'),
    path('delete/<int:pk>/', ProductDelete.as_view(), name='product-delete'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('category/<int:pk>/', CategoryList.as_view(), name='category'),
    path('comment/<int:pk>/', CommentList.as_view(), name='comment'),
    path('contact/<int:pk>/', ContactList.as_view(), name='contact'),
]
