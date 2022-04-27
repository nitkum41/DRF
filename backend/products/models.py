from django.conf import settings
from django.db import models
from django.db.models import Q
import random

User = settings.AUTH_USER_MODEL # auth.user in string
TAGS = ['electronics','cars','movies','boats','cameras']

class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self,query,user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs= self.is_public().filter(lookup) #only for public
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup) #for any
            qs = (qs | qs2).distinct() 
        return qs





class ProductManager(models.Manager):

    def get_queryset(self,*args,**kwargs):
        return ProductQuerySet(self.model, using=self._db)  #link model and the database to custom queryset

    def search(self,query, user=None):
        return self.get_queryset().search(query,user=user) #call methods in the custom queryset
                               






class Product(models.Model):
    #pk
    user = models.ForeignKey(User,default=1,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=15,decimal_places=2,default=99.99)

    #for search 
    public = models.BooleanField(default=True)

    #link objects to product manager class so its method can run on every query set
    objects = ProductManager()

    def is_public(self)-> bool:
        return self.bool
    
    def get_tags_list(self):
        return [random.choice(TAGS)]  #implement extra filter

    @property
    def path(self):
        return f"/products/{self.pk}"

    def get_absolute_url(self):
        return f"/api/products/{self.pk}/"
    
    @property
    def endpoint(self):
        return self.get_absolute_url()

    @property
    def body(self):
        return self.content

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price)*.8)

    def get_discount(self):
        return "10"
