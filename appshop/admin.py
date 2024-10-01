from django.contrib import admin
from django.contrib.auth.models import User
from .models import Contact, Category, Product, Size, Cart, Comment, Profile, Order, OrderItem


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'created'
    ordering = ('created',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created')
    list_filter = ('created',)
    search_fields = ('name', 'email')
    date_hierarchy = 'created'
    ordering = ('created',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'created')
    list_filter = ('created',)
    search_fields = ('name',)
    date_hierarchy = 'created'
    ordering = ('created',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category', 'created', 'updated', 'available')
    search_fields = ('name', 'category')
    date_hierarchy = 'created'
    ordering = ('created',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'quantity', 'created')
    list_filter = ('created',)
    search_fields = ('product', 'user')
    date_hierarchy = 'created'
    ordering = ('created',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created')
    list_filter = ('created',)
    search_fields = ('product', 'user')
    date_hierarchy = 'created'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')
    list_filter = ('created', )
    search_fields = ('user',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order', 'product')
