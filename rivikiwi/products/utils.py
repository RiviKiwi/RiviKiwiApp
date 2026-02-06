from .models import Product

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Value


def q_search(query):
    vector = SearchVector("name", "description", config='russian')
    query = SearchQuery(query, config='russian')
    result = (
        Product.objects.annotate(
            rank=SearchRank(
                vector,
                query,
                normalization=Value(2).bitor(Value(4)),
            )
        )
        .filter(rank__gt=0)
        .order_by("-rank")
    )
    return result

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



