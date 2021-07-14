from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import AcDetailsForm, UserForm,PasswordForm,AddressForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from KitchenChimney.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.template.loader import get_template
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from store.models import CheckOut,Cart,WishList
# Create your views here.
def account(request):

    form = UserForm()
    #variable for check wheather the user logged in or not it turns to True if logged in
    auth = None
    cart = False
    wishlist = False
    if request.method == 'POST':
        print('The request is post')
        #this step is for identify that from which form the request is coming so that we can create the user if the request is coming from register form
        if request.POST.get('action') == 'register':

            form = UserForm(request.POST)
            if form.is_valid():
    
                user_save = form.save()
                user_save.set_password(user_save.password)
                #set the is_active field to false for verifying the user email it only turns true when user verifyed his/her email
                user_save.is_active = False
                user_save.cart = Cart.objects.create(user=user_save)
                user_save.wishlist = WishList.objects.create(user=user_save)
                user_save.save()
                subject = "Please Verify your mail"
                #text template
                text_content = get_template('email/confirmation_plane.txt').render({'user':user_save})
                #html template
                html_content = get_template('email/confirmation_html.html').render({'user':user_save})
                recipient = str(request.POST.get('email'))
                msg = EmailMultiAlternatives(subject,text_content,EMAIL_HOST_USER,[recipient])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.info(request, "Your account is created. We've mailed you the verification link.")
                return render(request,'account/account.html',{'auth':auth,'form':form,'action':'register','wishlist':wishlist})
    
            else:
    
                return render(request,'account/account.html',{'auth':auth,'form':form,'action':'register','wishlist':wishlist})
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                auth = True
                print("redirected")
                return HttpResponseRedirect(reverse('account:account'))
            else:
                print('Invalid')
                messages.error(request,'Invalid credentails')
                return HttpResponseRedirect(request.path_info)
    else:
        if request.user.is_authenticated == True:
            cart = request.user.cart
            wishlist = request.user.wishlist
            auth = True
            return render(request,'account/account.html',{'auth':auth,'cart':cart,'wishlist':wishlist})
        else:
            auth = False
            return render(request,'account/account.html',{'auth':auth,'form':form,'cart':cart,'wishlist':wishlist})

#to activate the created user
def activate(request,ID):
    
    user = User.objects.get(id=ID)
    user.is_active = True
    user.save()
    subject = 'Account Activated'
    recipient = str(user.email)
    text_content = get_template('email/activated.txt').render()
    html_content = get_template('email/activated.html').render()
    msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [recipient])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    messages.info(request,'Your account is activated please login with your username and password')
    return HttpResponseRedirect(reverse('account:account'))

@login_required(redirect_field_name='account:account')
def orders(request):

    cart = False
    orders = False
    if request.user.is_authenticated == True:
        cart = request.user.cart
        wishlist = request.user.wishlist
        try:
            orders = request.user.ordercart_set.all()
        except:
            pass
        auth = True

    return render(request,'account/orders.html',{'auth':auth,'cart':cart,'orders':orders,'wishlist':wishlist})

@login_required(redirect_field_name='account:account')
def address(request):


    cart = request.user.cart
    auth = True
    wishlist = request.user.wishlist
    user = request.user
    try:
        user_check = user.address
    except:
        pass
    else:
        return render(request,'account/address.html',{'auth':auth,'address':user_check,'wishlist':wishlist,'cart':cart})
    return render(request,'account/address.html',{'auth':auth,'cart':cart,'wishlist':wishlist})

@login_required(redirect_field_name='account:account')
def ac_details(request):

    form = AcDetailsForm()
    cart = request.user.cart
    auth = True
    wishlist = request.user.wishlist
    if request.method == 'POST':
        print('ac_post')
        form = AcDetailsForm(request.POST)
        if form.is_valid():
            print('ac_valid')
            user = request.user
            try:
                check_user = user.customer
            except:
                ac_details = form.save(commit=False)
                ac_details.user = user
                ac_details.save()
                print("ac_created")
            else:
                check_user.first_name = form.cleaned_data['first_name']
                check_user.last_name = form.cleaned_data['last_name']
                check_user.save()
            messages.info(request, 'Saved Successfully')
            curr_pass = user.password
            curr_pass_entered = request.POST.get('current_password')
            if curr_pass_entered:
                matchcheck = check_password(curr_pass_entered, curr_pass)
                if matchcheck:
                    new_pass = request.POST.get('new_password')
                    user.set_password(new_pass)
                    user.save()
                    messages.info(request,'Password changed succesfully')
                    username = user.username
                    password = new_pass
                    user_auth = authenticate(username=username,password=password)
                    if user_auth is not None:
                        login(request, user_auth)
                else:
                    messages.error(request, "Cant't change the password. You entered a wrong password")
    return render(request,'account/ac_detail.html',{'auth':auth,'form':form,'cart':cart,'wishlist':wishlist})

@login_required(redirect_field_name='account:account')
def edit_address(request):

    form = AddressForm()
    cart = request.user.cart
    auth = True
    wishlist = request.user.wishlist
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            user = request.user
            try:
                check_user = user.address
            except:
                address = form.save(commit=False)
                address.user = user
                address.save()
            else:
                check_user.first_name = request.POST.get('first_name')
                check_user.last_name = request.POST.get('last_name')
                check_user.state = request.POST.get('state')
                check_user.street1 = request.POST.get('street1')
                check_user.street2 = request.POST.get('street2')
                check_user.city = request.POST.get('city')
                check_user.post_code = request.POST.get('post_code')
                check_user.phone = request.POST.get('phone')
                check_user.email = request.POST.get('email')
                check_user.save()
            messages.success(request,'Saved successfully')
            return HttpResponseRedirect(reverse('account:address'))
    try:
        check_user = request.user.address
    except:
        pass
    else:
        return render(request,'account/edit_address.html',{'auth':auth,'form':form,'address':check_user,'cart':cart,'wishlist':wishlist})
    return render(request,'account/edit_address.html',{'auth':auth,'form':form,'cart':cart,'wishlist':wishlist})

@login_required(redirect_field_name='account:account')
def track(request,ID):

    order = CheckOut.objects.get(id=ID)
    cart = request.user.cart
    auth = True
    wishlist = request.user.wishlist
    return render(request,'account/track_order.html',{'auth':auth,'cart':cart,'order':order,'wishlist':wishlist})

@login_required(redirect_field_name='account:account')
def log_out(request):

    logout(request)
    return HttpResponseRedirect(reverse('account:account'))

def lost_password(request,ID):

    form = PasswordForm()
    user = User.objects.get(id=ID)
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            return HttpResponseRedirect(reverse('account:account'))
    return render(request,'account/lost_password.html',{'form':form})

def forgot_mail(request):

    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST.get('username'))
        except:
            user = None
            messages.info(request,'No user found')
            return HttpResponseRedirect(request.path_info)
        else:
            subject = 'Reset Password'
            text_content = get_template('email/password_change.txt').render({'user':user})
            html_content = get_template('email/password_change.html').render({'user':user})
            recipient = str(user.email)
            msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.info(request,'Password change link sent to your registered email')
            return HttpResponseRedirect(request.path_info)
    return render(request,'account/forgot_password.html')

def return_item(request,ID):

    checkout = CheckOut.objects.get(id=ID)
    checkout.status = 'RT'
    checkout.save()
    messages.info(request,'Return succesfull')
    return HttpResponseRedirect(reverse('account:orders'))