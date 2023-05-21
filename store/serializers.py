from rest_framework import serializers
from .models import *

class AdsHomeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = AdsHome
        fields =['id','name','image']
class AdsSectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = AdsHome
        fields =['id','name','image']
class AdsListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = AdsHome
        fields =['id','name','image']

class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Company
        fields =['id','name','image']

#(used)
class SectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Section
        fields = ['id','name','image']
#
class SubSectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = SubSection
        fields = ['id','name','image']

class ListItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Item
        fields =['id','name','image','public_price','like']
#
class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    company=CompanySerializer()
    class Meta:
        model = Item
        fields =['id','name','effective_material','image','public_price','company','usage','description','warning','like']
#
class PrescriptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Prescription
        fields =['id','customer','image']

class ListDiscountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Item
        fields =['id','name','image','public_price','like','instead_of','percentage']

class ListOfferSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Item
        fields =['id','name','image','public_price','like','save_off']
class OfferSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    company=CompanySerializer()
    class Meta:
        model = Item
        fields =['id','name','effective_material','image','public_price','company','usage','description','warning','like','save_off']

class DiscountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    company=CompanySerializer()
    class Meta:
        model = Item
        fields =['id','name','effective_material','image','public_price','company','usage','description','warning','like','instead_of','percentage']


class LikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Item
        fields =['id','like']
class CartitemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product=ItemSerializer()
    sub_total=serializers.SerializerMethodField(method_name="total")
    class Meta:
        model = CartItems
        fields =['id','cart','product','quantity','sub_total']
    def total(self,cartitem:CartItems):
        return cartitem.quantity * cartitem.product.public_price
#used
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    #
    def validate_product_id(self, value):
        if not Item.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        return value
    #
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"] 
        quantity = self.validated_data["quantity"] 
        #
        try:
            cartitem = CartItems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except:
            self.instance = CartItems.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance
        
    class Meta:
        model = CartItems
        fields = ["id", "product_id", "quantity"]
#used
class UpdateCartitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields =['quantity']


class DoctorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Doctor
        fields =['id','name','image','spa','phone_number']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    items = CartitemSerializer(many=True)
    grand_total = serializers.SerializerMethodField(method_name="main_total")
    delivery_total = serializers.SerializerMethodField(method_name="main_delivery_total")
    master_total = serializers.SerializerMethodField(method_name="main_master_total")

    class Meta:
        model = Cart
        fields = ['id', 'items', 'grand_total', 'delivery_total', 'master_total']

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([float(item.quantity)*float(item.product.public_price) for item in items])
        return total

    def main_delivery_total(self, cart: Cart):
        user = self.context['request'].user
        total = float(user.country.delivery_cost)+float(user.city.delivery_cost)
        return total

    def main_master_total(self, cart: Cart):
        return self.main_total(cart) + self.main_delivery_total(cart)

class OrderSerializer(serializers.ModelSerializer):
    #cart=CartSerializer(many=False)
    #id = serializers.UUIDField()
    class Meta:
        model = Order
        fields =['customer','cart',]

class OrdersByCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderBranchSerializer(serializers.ModelSerializer):
    #cart=CartSerializer(many=False)
    #id = serializers.UUIDField()
    class Meta:
        model = Order
        fields =['customer','cart','created','Pharmacy',]