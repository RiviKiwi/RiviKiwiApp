from .models import Product
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Value


def q_search(query):
    vector = SearchVector("name", "description")
    query = SearchQuery(query)
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
