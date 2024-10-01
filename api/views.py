from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from appshop.models import Product
from .serializer import ProductSerializer, CategorySerializer, CommentSerializer, ContactSerializer
from rest_framework import permissions
from .permission import IsOwner



class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductListCreate(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDelete(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = CategorySerializer

class CommentList(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = CommentSerializer

class ContactList(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ContactSerializer
