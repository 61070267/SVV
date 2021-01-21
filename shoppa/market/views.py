import json
import keyword
from fnmatch import filter

from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import redirect, render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import (CustomerForm, CustomPasswordChangeForm,
                    CustomUserChangeForm, CustomUserCreationForm, PaymentForm,
                    ShopOwnerForm)
from .models import (Cart, CartItem, Category, Customer, Payment, Product,
                     ShopOwner, SubCategory)
from .serializers import (CartItemSerializer, CartSerializer,
                          CategorySerializer, PaymentSerializer,
                          ProductSerializer, SubCategorySerializer)


# Create your views here.
def index(request):
    context = {}
    # context['keyword'] = keyword
    # product = Product.objects.filter(name__icontains=keyword)
    if request.user.is_authenticated:
        user = request.user

        if user.groups.filter(name="Seller").exists():
            print('Seller Index')
            context['usertype'] = "Seller"

            #shop = ShopOwner.objects.get(pk=user)
            #productBox = Product.objects.filter(shop=shop)
            #context['productBox'] = productBox
        
        elif user.groups.filter(name="Buyer").exists():
            print('Buyer Index')
            context['usertype'] = "Buyer"
    
    else:
        print('Guest Index')
        context['usertype'] = "Guest"

    return render(request, template_name="market/index.html", context = context)

@api_view(['GET', 'POST'])
def index_api(request):
    if request.user.is_authenticated:
        user = request.user
        if user.groups.filter(name="Seller").exists():
            #Seller api
            shop = ShopOwner.objects.get(pk=request.user)
            if request.method == "GET":
                #print("get")
                if request.GET.get("shop"):
                    product = Product.objects.filter(shop=shop)
                    serializer = ProductSerializer(product, many=True)
                else:
                    product = Product.objects.create(shop=shop)
                    #product.img
                    serializer = ProductSerializer(product)
                #content = JSONRenderer().render(serializer.data)
                return Response(serializer.data)

    if request.method == "GET":
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


def product(request, product_id):
    context = {}
    product = Product.objects.get(pk=product_id)
    by_shop =  ShopOwner.objects.get(pk=product.shop)
    context['shop'] = by_shop
    context['product_id'] = product_id
    if request.user.is_authenticated:
        user = request.user
        if user.groups.filter(name="Seller").exists():
            #print(by_shop.username)
            print(user.username)
    
    return render(request, template_name="market/product.html", context = context)

@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def product_api(request):
    parser_classes = (FileUploadParser,)
    if request.method == "GET":
        product_id = request.GET.get("product_id")
        product = Product.objects.get(pk=product_id)
        #product_id = request.GET.get('product_id')
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=201)

    if request.user.is_authenticated:
        user = request.user
        #product = Product.objects.get(pk=request.data.get('id'))
        product_id = request.data.get('product_id')
        product = Product.objects.get(pk=product_id)
        by_shop =  ShopOwner.objects.get(pk=product.shop)
        if by_shop.username.username ==  user.username:
            if request.method == "PUT":
                serializer = ProductSerializer(product, data=request.data)
                #print(request.data.get('category'))
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
            
            if request.method == "DELETE":
                product = Product.objects.get(pk=product_id)
                product.delete()
                return Response({}, status=201)
    
    return JsonResponse({}, status=403)

@api_view(['GET'])
def category_api(request):
    if request.method == "GET":
        if request.GET.get("category_id"):
            category = request.GET.get("category_id")
            sub_category = SubCategory.objects.filter(category=category)
            serializer = SubCategorySerializer(sub_category, many=True)
        else:
            category = Category.objects.all()
            serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    return JsonResponse({}, status=403)

def catalog(request):
    return render(request, template_name="market/catalog.html")

@login_required
def cart(request):
    context = {}
    payform = PaymentForm()
    context['payform'] = payform
    return render(request, template_name="market/cart.html", context=context)

@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def cart_api(request):
    customer = Customer.objects.get(pk=request.user)
    cart = Cart.objects.filter(customer_username=customer, date=None).first()
    if request.method == "GET":
        if request.GET.get("cart_id"):
            cartId = request.GET.get("cart_id")
            cart_history = Cart.objects.get(customer_username=customer, pk=cartId)
            serializer = CartSerializer(cart_history)
            return JsonResponse(serializer.data)
        elif request.GET.get("cart_item"):
            cart_item = request.GET.get("cart_item")
            if cart_item != 'true':
                cart = Cart.objects.filter(customer_username=customer, pk=cart_item).first()
            cart_items = CartItem.objects.filter(cart_id=cart.pk)
            serializer = CartItemSerializer(cart_items, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            serializer = CartSerializer(cart)
            return JsonResponse(serializer.data)

    product_id = request.data.get('product_id')
    if request.method == "POST":
        request.data.update({'cart_id': cart.pk})
        #Already had this item in cart
        if CartItem.objects.filter(product_id=product_id, cart_id=cart.pk).exists():
            cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart.pk)
            quantity = cartitem.quantity + request.data.get('quantity')
            request.data.update({'quantity': quantity})
            print(request.data)
            serializer = CartItemSerializer(cartitem, data=request.data)
        else:
            request.data.update({'unit_price': Product.objects.get(pk=product_id).price})
            request.data.update({'item_price': Product.objects.get(pk=product_id).price * request.data.get('quantity')})
            serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == "PUT":
        #product_id = request.data.get('product_id')
        cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart.pk)
        request.data.update({'cart_id': cart.pk})
        serializer = CartItemSerializer(cartitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    if request.method == "DELETE":
        product_id = request.data.get('product_id')
        #cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart.pk)
        cartitem = CartItem.objects.filter(product_id=product_id, cart_id=cart.pk).first()
        cartitem.delete()
        return Response({})

def payment(request):
    context = {}
    return render(request, template_name="market/payment.html", context=context)

@api_view(['GET', 'PUT', 'POST'])
def pay_api(request):
    customer = Customer.objects.get(pk=request.user)
    cart = Cart.objects.filter(customer_username=customer, date=None).first()
    if request.method == "GET":
        cart_list = Cart.objects.filter(customer_username=customer, date__isnull=False)
        pay_list = Payment.objects.filter(cart_id__in=cart_list)
        serializer = PaymentSerializer(pay_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        request.data.update({'cart_id': cart.pk})
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cart.date = timezone.now()
            cart.save()
            new_cart = Cart.objects.create(customer_username=customer)
            new_cart.save()
            return Response(serializer.data)

    return Response(serializer.errors, status=400)

def search(request):
    context = {}
    if request.method == "GET":  
        if request.GET.get("catalog_id"):
            catalog_id = request.GET.get("catalog_id")
            context['catalog_id'] = catalog_id
        if request.GET.get("keyword"):
            keyword = request.GET.get("keyword")
            context['keyword'] = keyword
    return render(request, template_name="market/search.html", context=context)

@api_view(['GET', 'PUT'])
def search_api(request):
    if request.method == "GET":  
        if request.GET.get("catalog_id"):
            catalog_id = request.GET.get("catalog_id")
            subcategory = SubCategory.objects.get(pk=catalog_id)
            product = Product.objects.filter(category=subcategory)
            serializer = ProductSerializer(product, many=True)
            return JsonResponse(serializer.data, safe=False)
        if request.GET.get("keyword"):
            keyword = request.GET.get("keyword")
            product = Product.objects.filter(name__icontains=keyword)
            serializer = ProductSerializer(product, many=True)
            return JsonResponse(serializer.data, safe=False)
    return Response({})

@login_required
def account(request):
    context = {}
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            context["success"] = "Password Changed"
    
    if request.method == 'GET':
        form = CustomPasswordChangeForm(request.user)
    context['form'] = form
    return render(request, template_name="market/account.html", context=context, )

@login_required
def profile(request):
    context = {}
    user = request.user
    context['profile'] = user.username
    if user.groups.filter(name="Seller").exists():
        model = ShopOwner.objects.get(pk=user)
        form = ShopOwnerForm(instance=model)
        context['usertype'] = "Seller"
    elif user.groups.filter(name="Buyer").exists():
        model = Customer.objects.get(pk=user)
        form = CustomerForm(instance=model)
        context['usertype'] = "Buyer"
    context['form'] = form

    if request.method == 'POST':
        if user.groups.filter(name="Seller").exists():
            ExtraForm = ShopOwnerForm(request.POST, request.FILES, instance=model)
        elif user.groups.filter(name="Buyer").exists():
            ExtraForm = CustomerForm(request.POST, request.FILES, instance=model)
        if ExtraForm.is_valid():
            #Extra = ExtraForm.save(commit=False)
            #Extra.username = user
            #Extra.save()
            ExtraForm.save()
            return redirect("profile")
        else:
            context['error'] = ExtraForm.errors

    return render(request, template_name="market/profile.html", context = context)

def register(request):
    context = {}
    if request.method == 'POST':
        usertype = request.POST.get('usertype')
        Userform = CustomUserCreationForm(request.POST)
        if usertype == "Seller":
            ExtraForm = ShopOwnerForm(request.POST, request.FILES)
            group = Group.objects.get(name="Seller")
        else:
            ExtraForm = CustomerForm(request.POST, request.FILES)
            group = Group.objects.get(name="Buyer")

        if Userform.is_valid() and ExtraForm.is_valid():
            User = Userform.save()
            User.groups.add(group)
            User.save()
            Extra = ExtraForm.save(commit=False)
            Extra.username = User
            Extra.save()

            if usertype == "Buyer":
                cart = Cart.objects.create(customer_username=Extra)
                cart.save()

            username = Userform.cleaned_data.get('username')
            password = Userform.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        else:
            context['error'] = Userform.errors
            print('err')
            print(ExtraForm.errors)
    Userform = CustomUserCreationForm()
    #ShopForm = ShopOwnerForm()
    #CustForm = CustomerForm()
    context['Userform'] = Userform
    return render(request, template_name="market/register.html", context = context)

def register_api(request):
    response = ""
    if request.method == "GET":
        usertype = request.GET.get('usertype')
        if usertype == "Seller":
            response = ShopOwnerForm().as_p()
        else:
            response = CustomerForm().as_p()
        return HttpResponse(response, status=200)

    return HttpResponse(response, status=405)

def go_login(request):
    context = {}
    next_page = "index"
    
    if request.method == 'POST':
        if request.GET.get('next'): #check for redirect
            next_page = request.GET.get('next')
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            print(next_page)
            return redirect(next_page)
        else:
            context = {'username': username,
                       'password': password,
                       'error': 'Wrong username or password'}
    return render(request, template_name="market/login.html", context=context)

def go_logout(request):
    logout(request)
    return redirect("index")
