from django.db import models
from django.db.models.fields import BooleanField
from django.contrib.auth.models import User

class Product(models.Model):

    product_name = models.CharField(max_length=255)
    product_price = models.IntegerField()
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    in_stock = BooleanField()
    product_image = models.ImageField(upload_to='products')
    shipping = models.IntegerField()

    @property
    def imageURL(self):

        try:
            url = self.product_image.url
        except:
            url = ''
        return url

    def __str__(self):
        
        return self.product_name

class Cart(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def get_total(self):

        total = 0
        try:
            cart_items = self.cartitem_set.all()
        except:
            pass
        else:
            for item in cart_items:
                total += item.get_subtotal
        
        return total

    @property
    def total_shipping(self):

        total = 0
        try:
            cart_items = self.cartitem_set.all()
        except:
            pass
        else:
            for item in cart_items:
                total += item.product.shipping

        if self.get_total >= 1000:

            total = 0

        return total

    @property
    def final(self):

        total = self.get_total + self.total_shipping
        return total

    @property
    def cart_qty(self):

        count = 0
        try:
            cart_items = self.cartitem_set.all()
        except:
            pass
        else:
            count = len(cart_items)
        return count
    
    def __str__(self):

        return self.user.username

class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField()

    @property
    def get_subtotal(self):
        subtotal = self.product.product_price * self.qty

        return subtotal

    def __str__(self):

        return self.product.product_name
        
class OrderCart(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    @property
    def order_sub_total(self):

        item = self.ordercartitems_set.all()
        total = 0
        for i in item:

            total += i.item_total

        return total

    @property
    def order_shipping(self):

        item = self.ordercartitems_set.all()
        total = 0
        for i in item:

            total += i.product.shipping

        if self.order_sub_total > 1000:
            
            total = 0

        return total

    @property
    def final(self):

        return self.order_sub_total + self.order_shipping
    
class OrderCartItems(models.Model):

    ordercart = models.ForeignKey(OrderCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()

    @property
    def item_total(self):

        total = self.product.product_price * self.qty

        return total

class CheckOut(models.Model):

    STATE_CHOICES = [('KL','Kerala'),('TN','Tamilnadu'),('AP','Andrapradesh'),('KA','Karnataka'),('MA','Maharashtra'),('DL','Delhi')]
    STATUS_CHOICES = [('PL','Placed'),('CN','Canceled'),('PR','Processing'),('CO','Completed'),('RT','Returned')]
    PAYMENT = [('CA','Cash on delivery'),('CR','Pay with Card')]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    state = models.CharField(max_length=2,choices=STATE_CHOICES)
    street1 = models.CharField(max_length=255, blank=True, null=True)
    street2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    post_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField()
    items = models.OneToOneField(OrderCart,on_delete=models.CASCADE)
    status = models.CharField(max_length=2,choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=2,choices=PAYMENT)
    checkout_date = models.DateField(auto_now_add=True)

    def __str__(self):

        return str(self.id)

class WishList(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    @property
    def get_wishlist(self):

        total = 0
        try:
            items = self.wishlistitem_set.all()
        except:
            pass
        else:
            total = len(items)

        return total
        
    def __str__(self):

        return self.user.username

class WishListItem(models.Model):

    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):

        return self.wishlist.user.username



