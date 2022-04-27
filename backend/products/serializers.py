from rest_framework import serializers 
from rest_framework.reverse import reverse
from .models import Product
from api.serializers import UserPublicSerializer #serializer for username declared in api
from .validators import validate_title_no_hello,unique_product_title






class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail', #as mentioned in url path
        lookup_field ='pk',
        read_only=True
    )

    title = serializers.CharField(read_only=True)







#use model serializer when we need to perform create and update otrherwise for public display use only serializers

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user',read_only=True)

    #foreign key
    # related_products = ProductInlineSerializer(source='user.product_set.all',read_only=True, many=True)
    # discount = serializers.SerializerMethodField(read_only=True)
    
    # url = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    
    #it works on only model serializer(hyperlink)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field ='pk'
    )
    #  if we want to add arbitrary data to our model not previously defined
    # email = serializers.EmailField(write_only=True)


    # external validators
    title = serializers.CharField(validators=[validate_title_no_hello,unique_product_title])
    # identical field
    # name = serializers.CharField(source='title',read_only=True)

    body = serializers.CharField(source='content')
    class Meta:
        model = Product
        fields =[
            'owner',
            'pk',
            'url',
            'edit_url',
            # 'email',
            'title' ,
            # 'name',
            'body',
            'price',
            'sale_price',
            'public',
            'path',
            'endpoint'
            # 'discount',
            # 'related_products',
            ]

    # handling arbitrary data 
    # # when no instance create is called
    # def create(self,validated_data):
    #     # return Product.objects.create(**validated_data)
    #     # email = validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     return obj

    # #if instance update is called
    # def update(self,instance,validated_data):
    #     instance.title = validated_data.get('title')
    #     email = validated_data.pop('email')
    #     return super.update(instance,validated_data)



    # it works on all serializers
    def get_edit_url(self,obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit",kwargs={"pk":obj.pk},request=request)
    # def get_url(self,obj):
    #     request = self.context.get('request')
    #     if request is None:
    #         return None
    #     return reverse("product-detail",kwargs={"pk":obj.pk},request=request)
   
   
   
    # def get_discount(self,obj):
    #     if not hasattr(obj,'id'):
    #         return None
    #     if not isinstance(obj,Product):
    #         return None

    #     return obj.get_discount()

    # custom validation 
    # not for read only data
    # def validate_title(self,value):
    #     qs = Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already present")
    #     return value
