from django.urls import reverse_lazy
from .models import Product, ProductCategory, ProductImage, ProductView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import q_search, get_client_ip
from .forms import AddProductForm
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from common.mixins import ProductMixin


class IndexView(ListView):
    model = Product
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


class AddProductView(LoginRequiredMixin, ProductMixin, CreateView):
    template_name = "products/product_add_form.html"
    form_class = AddProductForm

    def get_success_url(self):
        return reverse_lazy("catalog:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditProductView(LoginRequiredMixin, ProductMixin, UpdateView):
    model = Product
    template_name = "products/product_add_form.html"
    form_class = AddProductForm
    slug_field = "slug"
    slug_url_kwarg = "product_slug"

    def get_object(self, queryset=None):
        return Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))

    def get_success_url(self):
        return reverse_lazy("catalog:home")

    def delete_old_images(self):
        old_images = ProductImage.objects.filter(
            product__slug=self.kwargs.get(self.slug_url_kwarg)
        )
        old_images.delete()

    def get_context_data(self, **kwargs):
        self.delete_old_images()
        context = super().get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super().get_initial()
        product = self.get_object()
        initial.update(
            {
                "name": product.name,
                "category": product.category,
                "description": product.description,
                "price": product.price,
                "discount": product.discount,
                "city": product.city,
            }
        )
        return initial


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")
    slug_field = "slug"
    slug_url_kwarg = "product_slug"

    def get_object(self, queryset=None):
        return Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
