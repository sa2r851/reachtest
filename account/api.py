from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response


#
class PharmacyRegistration(generics.CreateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
#
class CustomerRegistration(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
#
@api_view(['GET'])
def branch_cities(request,branch):
    details=City.objects.filter(branch__id=branch)
    data=CitySerializer(details,many=True).data
    return Response({'data':data})
#
@api_view(['GET'])
def city_customer(request,city):
    details=Customer.objects.filter(city__id=city)
    data=CustomerDetailsSerializer(details,many=True).data
    return Response({'data':data})
#
@api_view(['GET'])
def branch_staff(request):
    user=request.user
    details=Branch.objects.filter(staff=user)
    data=Branch_StaffSerializer(details,many=True).data
    return Response({'data':data})

@api_view(['GET'])
def Cities(request):
    details=City.objects.all()
    data=CitySerializer(details,many=True).data
    return Response({'data':data})