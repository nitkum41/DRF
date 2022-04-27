from django.forms.models import model_to_dict

from rest_framework.response  import Response
from rest_framework.decorators import api_view
from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.
@api_view(["POST"])
def api_home(request,*args,**kwargs):

    # instance = Product.objects.all().order_by("?").first()
    # data={}
    # if instance:
    #     # data=model_to_dict(model_data,fields=["id","title","price"])
    #     data = ProductSerializer(instance).data

    serializer = ProductSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        print(type(instance))
        data = ProductSerializer(instance).data
        return Response(data)

    return Response({"Error":"invalid data"},400)