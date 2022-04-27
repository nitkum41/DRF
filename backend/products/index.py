from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Product
#filter data from our app to algolia


@register(Product)
class ProductIndex(AlgoliaIndex):
    # should_public = 'is_public' # filtering done babed on is_public value
    
    #displayed results have the following fields
    fields=[
        'title',
        'body',
        'price',
        'user',
        'public',
        'path',
        'endpoint'

    ]
    settings = {
        'searchableAttributes':['title','content'],
        'attributesForFaceting':['user','public']
    }
    tags = 'get_tags_list'  #query to filter additional to other mentioned fields