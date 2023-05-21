from django.db import models
from account.models import Pharmacy ,Customer,Branch
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
SPA_CHOICES=[
    ('قلب', 'قلب'),

]
SHAPE_CHOICES = [
    ('افلام', 'افلام'),
    ('اقراص', 'اقراص'),
    ('اكياس', 'اكياس'),
    ('امبولات', 'امبولات'),
    ('اسبراي', 'اسبراي'),
    ('اسبراي الانف', 'اسبراي الانف'),
    ('اسبراي الفم', 'اسبراي الفم'),
    ('اقراص استحلاب', 'اقراص استحلاب'),
    ('اقماع شرجية', 'اقماع شرجية'),
    ('اقماع مهبلية', 'اقماع مهبلية'),
    ('المحلول', 'المحلول'),
    ('برطمان', 'برطمان'),
    ('بلسم', 'بلسم'),
    ('بودرة', 'بودرة'),
    ('بودرة استنشاق', 'بودرة استنشاق'),
    ('جل', 'جل'),
    ('جل للعين', 'جل للعين'),
    ('جل مهبلي', 'جل مهبلي'),
    ('حبيبات فوارة', 'حبيبات فوارة'),
    ('حقنة معباة', 'حقنة معباه'),
    ('حليب مجفف', 'حليب مجفف'),
    ('خرطوشة', 'خرطوشة'),
    ('رغوة', 'رغوة'),
    ('زيت', 'زيت'),
    ('سائل', 'سائل'),
    ('شامبو', 'شامبو'),
    ('شراب', 'شراب'),
    ('صابون', 'صابون'),
    ('غسول للفم', 'غسول للفم'),
    ('غسول مهبلي', 'غسول مهبلي'),
    ('فيال', 'فيال'),
    ('قطرة انف', 'قطرة انف'),
    ('قطرة الاذن', 'قطرة الاذن'),
    ('قطرة للعين', 'قطرة للعين'),
    ('قطعة', 'قطعة'),
    ('قلم معبأ', 'قلم معبأ'),
    ('كبسولات', 'كبسولات'),
    ('كريم', 'كريم'),
    ('كريم مهبلي', 'كريم مهبلي'),
    ('لاصقات', 'لاصقات'),
    ('لوشن', 'لوشن'),
    ('لولب', 'لولب'),
    ('محلول استنشاق', 'محلول استنشاق'),
    ('محلول شرجي', 'محلول شرجي'),
    ('محلول وريدي', 'محلول وريدي'),
    ('مرهم', 'مرهم'),
    ('مرهم شرجي', 'مرهم شرجي'),
    ('مرهم للعين', 'مرهم للعين'),
    ('مستحلب', 'مستحلب'),
    ('معجون اسنان', 'معجون اسنان'),
    ('معلق', 'معلق'),
    ('نقط فم', 'نقط فم'),
]
#
LETTER_CHOICES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
    ('H', 'H'),
    ('I', 'I'),
    ('J', 'J'),
    ('K', 'K'),
    ('L', 'L'),
    ('M', 'M'),
    ('N', 'N'),
    ('O', 'O'),
    ('P', 'P'),
    ('Q', 'Q'),
    ('R', 'R'),
    ('S', 'S'),
    ('T', 'T'),
    ('U', 'U'),
    ('V', 'V'),
    ('W', 'W'),
    ('X', 'X'),
    ('Y', 'Y'),
    ('Z', 'Z'),
]
#ads home
class AdsHome(models.Model):
    name=models.CharField(max_length=50,)
    image=models.ImageField(blank = True, null=True, default='')
    def __str__(self):
        return self.name    
#
#ads subsection
class AdsSubsection(models.Model):
    name=models.CharField(max_length=50,)
    image=models.ImageField(blank = True, null=True, default='')
    def __str__(self):
        return self.name    
#ads list products
class Adslist(models.Model):
    name=models.CharField(max_length=50,)
    image=models.ImageField(blank = True, null=True, default='')
    def __str__(self):
        return self.name    
#
class Company(models.Model):
    name=models.CharField(max_length=50,)
    image=models.ImageField(blank = True, null=True, default='')
    def __str__(self):
        return self.name
#
class Section(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(blank = True, null=True, default='')
    def __str__(self):
        return self.name
#
class SubSection(models.Model):
    name=models.CharField(max_length=50)
    section=models.ForeignKey(Section,on_delete=models.CASCADE)
    image=models.ImageField(blank = True, null=True, default='')
    def __str__(self):
        return self.name
#
class Item(models.Model):
    name=models.CharField(max_length=50)
    e_name = models.CharField(max_length=50)
    effective_material=models.CharField(max_length=100,default='المادة الفعالة')
    image=models.ImageField(blank = True, null=True, default='')
    usage=models.TextField(max_length=200,default='الاستخدام')
    description=models.TextField(max_length=300,default='الوصف')
    warning=models.TextField(max_length=300,default='لا يوجد تحذيرات')
    public_price=models.FloatField(default=100.00)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    section=models.ForeignKey(Section,on_delete=models.CASCADE)
    subsection=models.ForeignKey(SubSection,on_delete=models.CASCADE)
    letter= models.CharField(max_length=20,choices=LETTER_CHOICES)
    shape= models.CharField(max_length=20,choices=SHAPE_CHOICES)
    like=models.ManyToManyField(Customer,blank=True)
    discount = models.BooleanField(default=False)
    instead_of=models.FloatField(default=100.00)
    percentage=models.FloatField(default=10)
    offer = models.BooleanField(default=False)
    save_off=models.FloatField(default=100.00)
    out_of_stock=models.BooleanField(default=False)

    def __str__(self):
        return self.name
#
class Prescription(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='prescription')
    image=models.ImageField(blank = True, null=True, default='')
#
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='cart', null=True, default=None)
    created=models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
#
@receiver(post_save, sender=Customer)
def create_user_cart(sender, instance, created, **kwargs):
    if created and instance.role == "CUSTOMER":
        Cart.objects.create(customer=instance)
#
class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING,related_name='items')
    product =  models.ForeignKey(Item, on_delete=models.CASCADE,related_name='carditems')
    quantity = models.PositiveSmallIntegerField(default=0)
    @property
    def get_total(self):
        total = self.quantity * self.product.public_price
        if total == 0.00:
            self.delete()
        return total
    def __str__(self):
        return self.product.name
#
class Order(models.Model):
    Pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE,related_name='order_pharmacy', null=True, default=None)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='order_customer', null=True, default=None)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING,related_name='order')
    created=models.DateTimeField(auto_now_add=True)
    is_received = models.BooleanField(default=False)
#
class OrderItems(models.Model):
    Pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE,related_name='branch', null=True, default=None)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='orderitems')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
#
class Doctor(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,related_name='doctors')
    name=models.CharField(max_length=50)
    spa= models.CharField(max_length=20,choices=SPA_CHOICES)
    phone_number = PhoneNumberField(blank=True)
    image=models.ImageField(blank = True, null=True, default='')
