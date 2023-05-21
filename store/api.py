from .models import *
from .serializers import *
from django.http import JsonResponse
from account.models import *
from rest_framework import generics,viewsets ,status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib import messages
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet ,ModelViewSet
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.mixins import CreateModelMixin , RetrieveModelMixin ,DestroyModelMixin ,ListModelMixin
# add Prescription
class PrescriptionRegistration(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer
    def get_queryset(self):
        user = self.request.user
        return Prescription.objects.filter(customer=user)
# ads home
class AdsHomeView(generics.ListAPIView):
    queryset = AdsHome.objects.all()[:5]
    serializer_class = AdsHomeSerializer
# ads section
class AdsSectionView(generics.ListAPIView):
    queryset = AdsSubsection.objects.all()[:5]
    serializer_class = AdsSectionSerializer
# ads list
class AdsListView(generics.ListAPIView):
    queryset = Adslist.objects.all()[:5]
    serializer_class = AdsListSerializer
# samples Company
class SamplesCompanyView(generics.ListAPIView):
    queryset = Company.objects.all()[:5]
    serializer_class = CompanySerializer
# Company List
class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['name']
    pagination_class=PageNumberPagination
# samples offer
class SamplesOfferView(generics.ListAPIView):
    queryset = Item.objects.filter(offer=True)[:5]
    serializer_class = ListOfferSerializer
# All Offer
class ListOfferView(generics.ListAPIView):
    queryset = Item.objects.filter(offer=True)
    serializer_class = ListOfferSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['name','e_name','effective_material','company__name']
    filterset_fields = ['shape','letter','section']  
    pagination_class=PageNumberPagination
# samples Discount
class SamplesDiscounView(generics.ListAPIView):
    queryset = Item.objects.filter(discount=True)[:5]
    serializer_class = ListDiscountSerializer
# All Discounts
class ListDiscountView(generics.ListAPIView):
    queryset = Item.objects.filter(discount=True)
    serializer_class = ListOfferSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['name','e_name','effective_material','company__name']
    filterset_fields = ['shape','letter','section']  
    pagination_class=PageNumberPagination
#
@api_view(['GET'])
def products_campany(request,company):
    details=Item.objects.filter(company__id=company)
    data=ListItemSerializer(details,many=True).data
    return Response({'data':data})
# Categories List
class ListCategoriesView(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
#
@api_view(['GET'])
def Item_details(request,id):
    details=Item.objects.filter(id=id)
    data=ItemSerializer(details,many=False).data
    return Response({'data':data})
#
@api_view(['GET'])
def Item_Offer(request,id):
    details=Item.objects.filter(id=id)
    data=OfferSerializer(details,many=False).data
    return Response({'data':data})
#
@api_view(['GET'])
def Item_Discount(request,id):
    details=Item.objects.filter(id=id)
    data=DiscountSerializer(details,many=False).data
    return Response({'data':data})
#
@api_view(['GET'])
def sub_category(request,section):
    details=SubSection.objects.filter(section__id=section)
    data=SubSectionSerializer(details,many=True).data
    return Response({'data':data})
#
@api_view(['GET'])
def sub_product(request,subsection):
    details=Item.objects.filter(subsection__id=subsection)
    data=ListItemSerializer(details,many=True).data
    return Response({'data':data})
# All Product List
class ListAllItemView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ListItemSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['name','e_name','effective_material','company__name']
    filterset_fields = ['shape','letter','section']  
    pagination_class=PageNumberPagination
#
@api_view(['GET'])
def list_doctor(request,branch):
    details=Doctor.objects.filter(branch__id=branch)
    data=DoctorSerializer(details,many=True).data
    return Response({'data':data})
#
@api_view(['POST'])
def Like_or_Unlike(request, id):
    details = Item.objects.get(id=id)
    data = LikeSerializer(details, many=False).data
    user = request.user.id
    user_exists = details.like.filter(id=user)
    if len(user_exists) > 0:
        details.like.remove(user)
        print('removed')
    else:
        details.like.add(user)
        print('added')
    return Response({'data': data})
#
@api_view(['GET'])
def user_favourites(request):
    details=Item.objects.filter(like=request.user)
    data=ListItemSerializer(details,many=True).data
    return Response({'data':data})

class CartViewset(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names=['get','post','delete','patch']
    def get_queryset(self):
        return CartItems.objects.filter(cart_id=self.kwargs["cart_pk"])
    def get_serializer_class(self):
        if self.request.method=="POST":
            return AddCartItemSerializer
        elif self.request.method=="PATCH":
            return UpdateCartitemSerializer
        return CartitemSerializer
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

class OrdersByCustomer(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Order.objects.all()
    serializer_class = OrdersByCustomerSerializer
##############################
class Checkout(CreateModelMixin,GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_items_exists = CartItems.objects.filter(cart=serializer.validated_data['cart']).count()
        if cart_items_exists <= 0:
            return Response("Can't order an empty cart", status=422)

        customer_city = serializer.validated_data['customer'].city
        try:
            branch_object = City.objects.get(name=customer_city).branch
            serializer.validated_data['Pharmacy'] = branch_object.staff
        except ObjectDoesNotExist:
            return JsonResponse(data={'Error': 'City Not Found'}, status=422)
        ord_obj = serializer.save()
        cart_items = CartItems.objects.filter(cart=ord_obj.cart)
        #######add to order items#########
        order_items_list = []
        for item in cart_items:
            order_items_list.append(
                OrderItems(order=ord_obj,
                           cart=ord_obj.cart,
                           customer=ord_obj.customer,
                           product=item.product,
                           quantity=item.quantity),
            )
        OrderItems.objects.bulk_create(order_items_list)
        ##################################
        cart_items.delete()    ## cart
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def get_queryset(self,request,pk, *args, **kwargs):
        user =request.user
        queryset = [
            {'queryset': Cart.objects.get(id=pk,Pharmacy=user),
             'serializer_class': CartSerializer},
            {'queryset': CartItems.objects.filter(card=pk),
             'serializer_class': CartitemSerializer}
        ]
        return queryset