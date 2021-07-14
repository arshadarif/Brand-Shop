from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import CartItem, CheckOut, Product, OrderCart, OrderCartItems, WishList, WishListItem
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .forms import CheckOutForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from KitchenChimney.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.db.models import Q
# Create your views here.
def index(request):

    cart = False
    auth = False
    wishlist = False
    product = Product.objects.all()
    if request.user.is_authenticated == True:
        cart = request.user.cart
        auth = True
        wishlist = request.user.wishlist
    return render(request,'store/index.html',{'auth':auth,'products':product,'cart':cart,'wishlist':wishlist})

def contact(request):

    auth = False
    cart = False
    wishlist = False
    if request.user.is_authenticated == True:
        wishlist = request.user.wishlist
        cart = request.user.cart
        auth = True
    return render(request,'store/contact.html',{'auth':auth,'cart':cart,'wishlist':wishlist})

def privacy_policy(request):

    auth = False
    cart = False
    wishlist = False
    if request.user.is_authenticated == True:
        cart = request.user.cart
        wishlist = request.user.wishlist
        auth = True
    return render(request,'store/privacy_policy.html',{'auth':auth,'cart':cart,'wishlist':wishlist})

def about_us(request):

    wishlist = False
    auth = False
    cart = False
    if request.user.is_authenticated == True:
        wishlist = request.user.wishlist
        cart = request.user.cart
        auth = True
    return render(request,'store/about_us.html',{'auth':auth,'cart':cart,'wishlist':wishlist})

def product(request,ID):

    wishlist = False
    product = Product.objects.get(id=ID)
    auth = False
    cart = False
    if request.user.is_authenticated == True:
        wishlist = request.user.wishlist
        cart = request.user.cart
        auth = True
    return render(request,'store/product_page.html',{'auth':auth,'product':product,'cart':cart,'wishlist':wishlist})

def cart(request):

    if request.user.is_authenticated == True:
        cart = request.user.cart
        cart_items = CartItem.objects.filter(cart=cart)
        auth = True
        wishlist = request.user.wishlist
        return render(request,'store/cart.html',{'auth':auth,'cart_items':cart_items,'cart':cart,'wishlist':wishlist})
    else:
        messages.add_message(request, messages.ERROR, 'Please login to use cart')
        messages.add_message(request, messages.INFO, "Don't have an account? click on the register button to register a new account.It's easy and free")
        return HttpResponseRedirect(reverse('account:account'))

def checkout(request):

    if request.user.is_authenticated == True:
        form = CheckOutForm()
        try:
            check_address = request.user.address
        except:
            address = False
        else:
            address = check_address
        cart = request.user.cart
        wishlist = request.user.wishlist
        cart_items = CartItem.objects.filter(cart=cart)
        auth = True
        if cart.cart_qty == 0:
            return HttpResponseRedirect(reverse('store:cart'))
        if request.method == 'POST':
            form = CheckOutForm(request.POST)
            if form.is_valid() and request.user.is_authenticated == True:
                print("Valid")
                order_cart = OrderCart.objects.create(user=request.user)
                order_cart.save()
                cart = request.user.cart
                cartitems = cart.cartitem_set.all()
                for item in cartitems:
                    product = item.product
                    qty = item.qty
                    OrderCartItems.objects.create(ordercart=order_cart,product=product,qty=qty)
                checkout = form.save(commit=False)
                checkout.amount = request.user.cart.final
                checkout.status = 'PL'
                checkout.payment_method = request.POST.get('method')
                checkout.items = order_cart
                checkout.save()
                items = order_cart.ordercartitems_set.all()
                for item in cartitems:
                    item.delete()
                context = {'user':request.user,'checkout':checkout,'cartitems':items,'order_cart':order_cart}
                text_content = get_template('email/order_placed.txt').render(context)
                html_content = get_template('email/order_placed.html').render(context)
                subject = 'Order Placed'
                recipient = str(request.user.email)
                msg = EmailMultiAlternatives(subject,text_content,EMAIL_HOST_USER,[recipient])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return render(request,'store/order_success.html',{'auth':auth,'cart':cart  ,    'checkout':checkout,'items':items,'wishlist':wishlist})
        return render(request,'store/checkout.html',{'auth':auth,'cart':cart,'address':address, 'form':form,'wishlist':wishlist})
    else:
        messages.error(request,'Please login first')
        return HttpResponseRedirect(reverse('account:account'))

def user_wishlist(request):

    if request.user.is_authenticated == True:
        cart = request.user.cart
        wishlist = request.user.wishlist
        wishlist_item = wishlist.wishlistitem_set.all()
        auth = True
        return render(request,'store/wishlist.html',{'auth':auth,'cart':cart,'wishlist':wishlist,'items':wishlist_item})
    else:
        messages.error(request,'Please login first')
        return HttpResponseRedirect(reverse('account:account'))

@csrf_exempt
def add_cart(request):
    
    data = json.loads(request.body)
    context = {}
    product = Product.objects.get(id=data['id'])
    cart = request.user.cart
    check = CartItem.objects.filter(cart=cart,product=product)
    if len(check) == 0:
        CartItem.objects.create(cart=cart, product=product, qty=1)
        context['msg'] = 'success'
        context['cart_qty'] = cart.cart_qty
    else:
        context['msg'] = 'already exist'
        context['cart_qty'] = cart.cart_qty
    return JsonResponse(context)

@csrf_exempt
def change_qty(request):

    cart = request.user.cart
    data = json.loads(request.body)
    product = Product.objects.get(id=data['item'])
    item = CartItem.objects.get(cart=cart,product=product)
    curr_qty = item.qty
    if data['action'] == 'add':
        item.qty = curr_qty + 1
    elif data['action'] == 'substract':
        if curr_qty > 1:
            item.qty = item.qty - 1
    item.save()
    context = {}
    context['msg'] = 'success'
    context['qty'] = item.qty
    context['subtotal'] = item.get_subtotal
    context['total'] = cart.get_total
    context['final'] = cart.final
    context['shipping'] = cart.total_shipping
    return JsonResponse(context)

@csrf_exempt
def add_wishlist(request):

    data = json.loads(request.body)
    wishlist = request.user.wishlist
    product = Product.objects.get(id=data['id'])
    check_wishlist = WishListItem.objects.filter(wishlist=wishlist, product=product)
    context = {}
    if len(check_wishlist) == 0:
        WishListItem.objects.create(wishlist=wishlist, product=product)
        context['msg'] = 'success'
    else:
        context['msg'] = 'already exist'
    context['qty'] = wishlist.get_wishlist
    return JsonResponse(context)

@csrf_exempt
def remove_wishlist(request):

    data = json.loads(request.body)
    wishlist = request.user.wishlist
    product = Product.objects.get(id=data['id'])
    context = {}
    try:
        item = WishListItem.objects.get(wishlist=wishlist, product=product)
    except:
        context['msg'] = 'wrong'
    else:
        item.delete()
        qty = wishlist.get_wishlist
        context['msg'] = 'success'
        context['qty'] = qty
    return JsonResponse(context)

@csrf_exempt
def remove_cart(request):

    data = json.loads(request.body)
    cart = request.user.cart
    product = Product.objects.get(id=data['id'])
    context = {}
    try:
        item = CartItem.objects.get(cart=cart, product=product)
    except:
        context['msg'] = 'wrong'
    else:
        item.delete()
        qty = cart.cart_qty
        context['msg'] = 'success'
        context['qty'] = qty
        context['subtotal'] = cart.get_total
        context['shipping'] = cart.total_shipping
        context['total'] = cart.final
    return JsonResponse(context)

@csrf_exempt
def search_ajax(request):

    data = json.loads(request.body)
    print(data)
    search = data['search']
    products = Product.objects.filter(Q(product_name__icontains=search))
    context = {}
    if len(products) > 0:
        context['content'] = True
        items = {}
        num = 1
        for i in products:
            print(i)
            item = {}
            item['url'] = f'/product/{i.id}'
            item['image'] = i.imageURL
            item['name'] = i.product_name
            item['price'] = i.product_price
            items[num] = item
            num += 1
        context['items'] = items
        print(context['items'])
    else:
        context['content'] = False
    return JsonResponse(context)

@csrf_exempt
def search(request):

    products = False
    if request.method == 'POST':
        
        item = request.POST.get('search_item')
        products = Product.objects.filter(Q(product_name__icontains=item))
    
    return render(request,'store/search.html',{'products':products})
