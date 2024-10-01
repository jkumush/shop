from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from .models import Contact, Category, Product, Size, Cart, Comment, Order, OrderItem, Profile
from django.views.decorators.csrf import csrf_exempt
from .forms import EditProfileForm
import json
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@staff_member_required
def AdminPage(request):
    orders = Order.objects.all()
    return render(request, 'adminpage.html', {'orders': orders})

@staff_member_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, 'Order deleted successfully!')
    return redirect('adminpage')

@staff_member_required
def delete_all_orders(request):
    Order.objects.all().delete()
    messages.success(request, 'All orders deleted successfully!')
    return redirect('adminpage')



@login_required
def Checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_sum = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_no = request.POST.get('mobile_no')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        payment_method = request.POST.get('payment')

        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            mobile_no=mobile_no,
            address=address,
            country=country,
            state=state,
            city=city,
            zip_code=zip_code,
            payment_method=payment_method,
            total_price=total_sum  
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            item.product.decrease_stock(item.quantity)
            item.delete()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('home')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_sum': total_sum})




def search(request):
    query = request.GET.get('q')
    if query:
        products_by_name = Product.objects.filter(name__icontains=query)
        
        categories = Category.objects.filter(name__icontains=query)
        products_by_category = Product.objects.filter(category__in=categories)
        
        products = products_by_name | products_by_category
    else:
        products = Product.objects.none()
    
    return render(request, 'search_results.html', {'products': products, 'query': query})



def CategoryPage(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)


    price_filters = request.GET.getlist('price')
    if price_filters:
        price_ranges = {
            '100': (0, 100),
            '200': (100, 200),
            '300': (200, 300),
            '400': (300, 400),
            '500': (400, 500),
        }
        price_query = Q()
        for price in price_filters:
            if price in price_ranges:
                min_price, max_price = price_ranges[price]
                price_query |= Q(price__gte=min_price, price__lt=max_price)
        products = products.filter(price_query)


    return render(request, 'dress.html', {'category': category, 'products': products})


def DressPage(request, gender):
    products = Product.objects.filter(gender=gender)
    out_of_stock_products = Product.objects.filter(gender=gender, stock__lte=0)


    return render(request, 'dress.html', {
        'out_of_stock_products': products,
        'gender': gender
    })



# def DressPage(request, gender):
#     products = Product.objects.filter(gender=gender)
#     out_of_stock_products = Product.objects.filter(gender=gender, stock__lte=0)
#     return render(request, 'dress.html', {'products': products, 'out_of_stock_products': out_of_stock_products, 'gender': gender})



@login_required
@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['product_id']
        action = data['action']

        cart_items = Cart.objects.filter(user=request.user, product_id=product_id)

        if not cart_items.exists():
            return JsonResponse({'success': False, 'error': 'Cart item not found'})

        cart_item = cart_items.first()
        product = cart_item.product

        if action == 'increase':
            if product.stock > 0:
                cart_item.quantity += 1
                product.decrease_stock(1)
            else:
                return JsonResponse({'success': False, 'error': 'Not enough stock'})
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
            product.increase_stock(1)
        elif action == 'remove':
            product.increase_stock(cart_item.quantity)
            cart_item.delete()
            return JsonResponse({'success': True})

        cart_item.save()

        total_price = cart_item.product.price * cart_item.quantity

        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity,
            'total_price': total_price
        })

    return JsonResponse({'success': False})


@login_required
def profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            profile_picture_url = request.user.profile.profile_picture.url if request.user.profile.profile_picture else None
            return JsonResponse({'success': True, 'profile_picture_url': profile_picture_url})
    else:
        form = EditProfileForm(instance=request.user.profile)
    return render(request, 'pfp.html', {'form': form})


# @login_required
# def profile_view(request):
#     user = request.user
#     context = {
#         'name': user.get_full_name() or '',
#         'username': user.username or '',
#         'email': user.email or '',
#         'phone_number': user.profile.phone_number if hasattr(user.profile, 'phone_number') else '',
#         'bio': user.profile.bio if hasattr(user.profile, 'bio') else ''
#     }
#     return render(request, 'pfp.html', context)


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user.first_name = request.POST.get('name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        profile.phone_number = request.POST.get('phone')
        profile.bio = request.POST.get('bio')
        user.save()
        profile.save()
        return redirect('home')

    context = {
        'name': user.first_name,
        'username': user.username,
        'email': user.email,
        'phone_number': profile.phone_number,
        'bio': profile.bio
    }
    return render(request, 'pfp.html', context)


@login_required
@csrf_exempt
def upload_profile_picture(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()
        return JsonResponse({'success': True, 'profile_picture_url': user_profile.profile_picture.url})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def remove_profile_picture(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        user_profile.profile_picture = 'profiles/def.jpg'
        user_profile.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})





def CommentPage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            comment = request.POST.get('comment')
            product = get_object_or_404(Product, id=product_id)
            a = Comment()
            a.product = product
            a.user = request.user
            a.message = comment
            a.save()
            return redirect('detail', slug=product.slug)
        else:
            return render(request, 'detail.html', {'comment': comment})
    else:
        return redirect('/login/')  

def Home(request):
    cats = Category.objects.all()
    category_product_counts = {category.id: Product.objects.filter(category=category).count() for category in cats}
    recent_products = Product.objects.order_by('-created')[:8]
    
    return render(request, 'index.html', {'cats': cats, 'category_product_counts': category_product_counts, 'recent_products': recent_products})

def CartPage(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_sum = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_sum': total_sum,
    }
    return render(request, 'cart.html', context)



def Detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    comments = Comment.objects.filter(product=product)
    comment_count = comments.count()
    user = product.user
    return render(request, 'detail.html', {'p': product, 'com': comments, 'product_user': user, 'comment_count': comment_count})
    






def Shop(request):
    return render(request, 'shop.html')

def ContactPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print(name)
        a = Contact()
        a.name=name
        a.email = email
        a.subject = subject
        a.message = message
        a.save()
        return redirect('contact')
    return render(request, 'contact.html')

def logindef(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            if 'signup' in request.POST:
                username = request.POST.get('username')
                email = request.POST.get('email')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                if password1 == password2:
                    if User.objects.filter(username=username).exists():
                        messages.error(request, 'This username is already taken')
                        return redirect('login')
                    elif User.objects.filter(email=email).exists():
                        messages.error(request, 'This email is already taken')
                        return redirect('login')
                    else:
                        user = User.objects.create_user(username=username, email=email, password=password1)
                        user.save()
                        login(request, user)
                        messages.success(request, "You are registered successfully")
                        return redirect('home')
                else:
                    messages.error(request, "The passwords didn't match")
                    return redirect('login')
            elif 'login' in request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)

                if user != None:
                    login(request, user)
                    return redirect('home')
                else:
                    print('Incorrect password or username')
                    messages.error(request, "Incorrect password or username")
                    return redirect('login')
        else:
            return render(request, 'login.html')

def Logout(request):
    logout(request)
    messages.info(request, "You logged out")
    return redirect('home')



@login_required
def add_to_cart(request, id):
    if request.method == 'POST':   
        if 'addtocart' in request.POST: 
            product_id = request.POST.get('product_id')
            size_id = request.POST.get('size')
            color = request.POST.get('color')
            quantity = int(request.POST.get('quantity'))

            print(f"Product ID: {product_id}, Size ID: {size_id}, Color: {color}, Quantity: {quantity}")

            product = get_object_or_404(Product, id=id)
            size = get_object_or_404(Size, id=size_id) if size_id else None

            cart_item, created = Cart.objects.get_or_create(
                product=product,
                size=size,
                color=color,
                user=request.user,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            product.decrease_stock(quantity)

    
            print(f"Cart Item: {cart_item}")

            return redirect('cart') 
    return redirect('home')