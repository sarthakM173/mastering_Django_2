from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter,SimpleRouter
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet)

products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')
cart_router=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',views.CartItemSet,basename='cart-items')

urlpatterns=[
    path('',include(router.urls)),
    path('',include(products_router.urls))
    # path('products/',views.ProductList.as_view()),
    # path('products/<int:id>/',views.ProductDetials.as_view()),
    # path('collections/',views.CollectionList.as_view()),
    # path('collections/<int:pk>/',views.CollectionDetails.as_view(),name='collection-detail')

]
