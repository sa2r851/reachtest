from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from . import api
from rest_framework_nested import routers
app_name='store'
router=DefaultRouter()
router.register('cart',api.CartViewset,basename='cart')
router.register('checkout',api.Checkout,basename='checkout')
router.register('orders',api.OrdersByCustomer,basename='orders')
cart_router=routers.NestedDefaultRouter(router,'cart',lookup="cart")
cart_router.register("items",api.CartItemViewSet,basename="cart_items")
urlpatterns = [
    path("",include(router.urls)),
    path("",include(cart_router.urls)),    
    # home
    ##ads
    path("adshome",api.AdsHomeView.as_view(),name='adshome'),
    path("adssection",api.AdsSectionView.as_view(),name='adssection'),
    path("adslist",api.AdsListView.as_view(),name='adslist'),
    ## filter
    path("filter",api.ListAllItemView.as_view(),name='filter'),
    ## brands
    path("samples_companies",api.SamplesCompanyView.as_view(),name='last companies'),
    path("companies",api.CompanyListView.as_view(),name='companies'),
    path("companies/<int:company>",api.products_campany,name='company-products'),
    ## offers
    path("samples_offers",api.SamplesOfferView.as_view(),name='last offer'),
    path("offers",api.ListOfferView.as_view(),name='offers'),    
    path("offers/<int:id>",api.Item_Offer,name='offer-details'),
    ## discounts
    path("samples_discount",api.SamplesDiscounView.as_view(),name='last discount'),
    path("discounts",api.ListDiscountView.as_view(),name='discounts'),    
    path("discounts/<int:id>",api.Item_Discount,name='discount-details'),
    ## sections
    path("categories",api.ListCategoriesView.as_view(),name='categories'),
    ## subsections
    path("subcategory/<int:section>",api.sub_category,name='sub-category'),
    ## list products
    path("subcategory/<int:subsectiom>",api.sub_product,name='sub-product'),
    ## product details
    path("subcategory/<int:id>",api.Item_details,name='product-details'),
    ## rosheta
    path('roshta/', api.PrescriptionRegistration.as_view(), name='roshta'),
    ## doctors
    path("categories",api.list_doctor,name='categories'),
    ## favourite
    path("list_fav",api.user_favourites,name='list fav'),
    path("list_fav/<int:id>",api.Like_or_Unlike,name='offer-details'),
    ## cart

    ## checkout
    ## list orders
    ## finish order
    ## past orders
    ##
]
