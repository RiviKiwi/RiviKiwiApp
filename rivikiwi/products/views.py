from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Product, ProductCategory, City, ProductImage, ProductView
from .utils import q_search, get_client_ip
from .forms import AddProductForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView


class IndexView(ListView):
    model=Product
    template_name = "products/index.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug", None)

        max_price = self.request.GET.get("max_price", None)
        min_price = self.request.GET.get("min_price", None)
        rating = self.request.GET.get("rating", None)
        has_discount = self.request.GET.get("has_discount", None)
        order_by = self.request.GET.get("order_by", None)
        city = self.request.GET.get("city", None)
        query = self.request.GET.get("q", None)

        # if not category_slug:
        #     category_slug = "all"

        category = (
            ProductCategory.objects.get(slug=category_slug) if category_slug else None
        )
        products = None

        if category_slug == "all" or (not query and not category_slug):
            products = super().get_queryset()
            category = ProductCategory.objects.get(slug="all")
        elif query:
            products = q_search(query)
        else:
            products = super().get_queryset().filter(category__slug=category_slug)

        if order_by:
            products = products.order_by(order_by)

        if city and city != "Любой город":
            products = products.filter(city__name=city)

        if min_price and min_price != "0":
            products = products.filter(price__gte=int(min_price))

        if max_price and max_price != "0":
            products = products.filter(price__lte=int(max_price))

        if rating:
            products = products.filter(rating__gte=float(rating))

        if has_discount:
            products = products.filter(discount__gt=0)

        self.category = category

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

class ProductViewController(DetailView):
    template_name = "products/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def check_is_view_exist(self, product):
        client_ip = get_client_ip(self.request)
        user = self.request.user
        if user.is_authenticated:
            ProductView.objects.get_or_create(
                product=product, user=user, ip_address=client_ip
            )
        else:
            ProductView.objects.get_or_create(product=product, ip_address=client_ip)

    def get_object(self, queryset=None):
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        self.check_is_view_exist(product)
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@login_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(data=request.POST)

        category_sl = request.POST.get("category")
        city_sl = request.POST.get("city")
        images = request.FILES.getlist("images")

        if len(images) < 10:
            if form.is_valid():
                new_form = form.save(commit=False)
                try:
                    category = ProductCategory.objects.get(slug=category_sl)
                    city = City.objects.get(slug=city_sl)
                    new_form.category = category
                    new_form.city = city
                    new_form.user = request.user
                    new_form.save()
                    for i, image in enumerate(images):
                        is_main = True if i == 0 else False
                        ProductImage.objects.create(
                            image=image, product=new_form, is_main=is_main
                        )
                    return HttpResponseRedirect(reverse("catalog:home"))
                except Exception:
                    print("wrong slug in category or city")
    else:
        form = AddProductForm()

    context = {
        "form": form,
    }

    return render(request, "products/product_add_form.html", context)
