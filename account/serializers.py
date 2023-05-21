from rest_framework import serializers
from .models import *
#
class PharmacySerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(default="PHARMACY")
    class Meta:
        model = Pharmacy
        fields=['username','city','country','password','address','phone_number','role']
    def create(self, validated_data):
        user = Pharmacy(
            username=validated_data['username'],
            city=validated_data['city'],
            country=validated_data['country'],
            address=validated_data['address'],
            phone_number=validated_data['phone_number'],)
        user.set_password(validated_data['password'])
        user.save()
        return user
#
class CustomerSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(default="CUSTOMER")
    class Meta:
        model = Customer
        fields=['username','city','country','password',"address",'phone_number','role']
    def create(self, validated_data):
        user = Customer(
            username=validated_data['username'],
            city=validated_data['city'],
            country=validated_data['country'],
            address=validated_data['address'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
#
class SimpleCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields=['id','name']
#
class SimpleCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields=['id','name']
#
class SimpleBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields=['id','name']
#
class CitySerializer(serializers.ModelSerializer):
    country=SimpleCountrySerializer(many=False)
    branch=SimpleCountrySerializer(many=False)
    class Meta:
        model = City
        fields = ['id','name','country','branch','delivery_cost']
#
class CustomerDetailsSerializer(serializers.ModelSerializer):
    country=SimpleCountrySerializer(many=False)
    city=SimpleCitySerializer(many=False)

    class Meta:
        model = Customer
        fields=['username','city','country',"address",'phone_number']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields=['id','username']
#
class Branch_StaffSerializer(serializers.ModelSerializer):
    staff=StaffSerializer(many=False)
    class Meta:
        model = Branch
        fields=['name','staff']

