from rest_framework import viewsets,mixins

from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field ='pk' #default

    '''
        by default all are available 

        get -> list-> queryset
        get-> retrieve-> detail view
        post-> create
        put-> update
        patch-> partial update
        delete-> destroy
    '''
   

class ProductGenericViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):
    '''
    limit number of default methhods available on the viwsets
    Here only list and retrieve
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field ='pk' #default

'''
it can be used in urls.py as with class based views also 

product_list_view = ProductGenericViewSet.as_view({'get':'list'})
product_detail_view = ProductGenericViewSet.as_view({'get':'retrieve'})
'''