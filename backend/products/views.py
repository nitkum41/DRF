from rest_framework import authentication , generics,mixins , permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Product
from api.permissions import IsStaffEditorPermission
from api.mixins import (
    StaffEditorPermissionMixin,
    UserQuerySetMixin)
from .serializers import ProductSerializer


from api.authentication import TokenAuthentication
# Create your views here.



# class based generic views
# create and list
class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     TokenAuthentication]
    #order of permissions matter too
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]

    def perform_create(self,serializer):
        # serializer.save(user=self.request.user)
        # email = serializer.validated_data.pop('email')
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=self.request.user,content=content)  # equivalent to form.save() model.save()

    #associate data to a particular user using queryset
    # def get_queryset(self,*args,**kwargs):
    #     qs = super().get_queryset(*args,**kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=request.user)

#detail view
class ProductDetailAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]


class ProductUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]


    def perform_update(self,serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDestroyAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]


    def perform_destroy(self,instance):
        super().perform_destroy(instance)
        


# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


### model mixins and generic class based view
class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self,request,*args,**kwargs):
        print(args,kwargs)  ## kwargs contains pk
        pk=kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request,*args,**kwargs)
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)



#function based views with serializers

@api_view(["GET","POST"])
def product_alt_view(request,pk=None,*args,**kwargs):
    method = request.method
    if method=="GET":
        if pk is not None:
            #detail view
            obj = get_object_or_404(Product,pk=pk)
            data = ProductSerializer(obj,many=False).data
            return Response(data)


        #list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset,many=True).data
        return Response(data)


    if method=="POST":
        # create view
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"Error":"invalids data"},status=400)