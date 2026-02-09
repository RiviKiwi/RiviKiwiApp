import logging
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
from users.models import User

logger = logging.getLogger("products_app")


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    paginate_by = 3

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug", None)
        logger.debug("Get category slug from request")
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
            logger.debug("Get all products fron DB")
        elif query:
            products = q_search(query)
            logger.debug("Search products by query")
        else:
            products = super().get_queryset().filter(category__slug=category_slug)
            logger.debug("Get products bu category slug")

        if order_by:
            products = products.order_by(order_by)
            logger.debug("Oreder products")

        if city and city != "Любой город":
            products = products.filter(city__name=city)
            logger.debug("Get products by city")

        if min_price and min_price != "0":
            products = products.filter(price__gte=int(min_price))
            logger.debug("Filter products by min price")

        if max_price and max_price != "0":
            products = products.filter(price__lte=int(max_price))
            logger.debug("Filter products by max price")

        if rating:
            users = [user for user in User.objects.all() if user.get_rating() >= float(rating)]
            products = products.filter(user__in=users)
            logger.debug("Filter products by rating")

        if has_discount:
            products = products.filter(discount__gt=0)
            logger.debug("Filter products by having discount")

        self.category = category
        logger.info("Products ready to context")
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        logger.debug("Set category to context")
        logger.info("Context ready")
        return context


class ProductViewController(DetailView):
    template_name = "products/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"

    def check_is_view_exist(self, product):
        client_ip = get_client_ip(self.request)
        user = self.request.user
        logger.debug(f"Checking view existence for product {product.id}")

        if user.is_authenticated:
            view, created = ProductView.objects.get_or_create(
                product=product, user=user, ip_address=client_ip
            )
            logger.debug(
                f"Authenticated view {'created' if created else 'exists'} for user {user.id}"
            )
        else:
            view, created = ProductView.objects.get_or_create(
                product=product, ip_address=client_ip, user=None
            )
            logger.debug(
                f"Anonymous view {'created' if created else 'exists'} for IP {client_ip}"
            )

    def get_object(self, queryset=None):
        logger.debug(
            f"Getting product with slug: {self.kwargs.get(self.slug_url_kwarg)}"
        )
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        logger.debug(f"Product {product.id} retrieved")
        self.check_is_view_exist(product)
        logger.info(f"Product {product.id} view recorded")
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.debug("Product context prepared")
        logger.info("Product view context ready")
        return context


class AddProductView(LoginRequiredMixin, ProductMixin, CreateView):
    template_name = "products/product_add_form.html"
    form_class = AddProductForm

    def get_success_url(self):
        logger.debug("Getting success URL for product creation")
        url = reverse_lazy("catalog:home")
        logger.info(f"Success URL resolved: {url}")
        return url

    def form_valid(self, form):
        logger.debug(f"AddProductView form valid for user {self.request.user.id}")
        response = super().form_valid(form)
        logger.info(
            f"Product reated successfully by user {self.request.user.id}"
        )
        return response

    def form_invalid(self, form):
        logger.debug(f"AddProductView form invalid for user {self.request.user.id}")
        logger.warning(f"Product creation form invalid: {form.errors}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.debug("Add product context prepared")
        logger.info("Add product view context ready")
        return context


class EditProductView(LoginRequiredMixin, ProductMixin, UpdateView):
    model = Product
    template_name = "products/product_add_form.html"
    form_class = AddProductForm
    slug_field = "slug"
    slug_url_kwarg = "product_slug"

    def get_object(self, queryset=None):
        logger.debug(
            f"Getting product for edit with slug: {self.kwargs.get(self.slug_url_kwarg)}"
        )
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        logger.debug(f"Product {product.id} retrieved for editing")
        return product

    def get_success_url(self):
        logger.debug("Getting success URL for product update")
        url = reverse_lazy("catalog:home")
        logger.info(f"Success URL resolved: {url}")
        return url

    def delete_old_images(self):
        logger.debug(
            f"Deleting old images for product {self.kwargs.get(self.slug_url_kwarg)}"
        )
        old_images = ProductImage.objects.filter(
            product__slug=self.kwargs.get(self.slug_url_kwarg)
        )
        image_count = old_images.count()
        old_images.delete()
        logger.info(
            f"Deleted {image_count} old images for product {self.kwargs.get(self.slug_url_kwarg)}"
        )

    def form_valid(self, form):
        logger.debug(f"EditProductView form valid for product {self.get_object().id}")
        response = super().form_valid(form)
        logger.info(
            f"Product {self.object.id} updated successfully by user {self.request.user.id}"
        )
        return response

    def form_invalid(self, form):
        logger.debug(f"EditProductView form invalid for product {self.get_object().id}")
        logger.warning(f"Product update form invalid: {form.errors}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        logger.debug("Preparing edit product context")
        self.delete_old_images()
        context = super().get_context_data(**kwargs)
        logger.debug("Edit product context prepared")
        logger.info("Edit product view context ready")
        return context

    def get_initial(self):
        logger.debug(f"Getting initial data for product {self.get_object().id}")
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
        logger.debug(f"Initial data prepared for product {product.id}")
        return initial


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")
    slug_field = "slug"
    slug_url_kwarg = "product_slug"

    def get_object(self, queryset=None):
        logger.debug(
            f"Getting product for deletion with slug: {self.kwargs.get(self.slug_url_kwarg)}"
        )
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        logger.debug(f"Product {product.id} retrieved for deletion")
        return product

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        logger.debug(f"Deleting product {product.id}")
        response = super().delete(request, *args, **kwargs)
        logger.info(
            f"Product {product.id} deleted successfully by user {self.request.user.id}"
        )
        return response

    def get_success_url(self):
        logger.debug("Getting success URL for product deletion")
        url = super().get_success_url()
        logger.info(f"Redirecting to {url} after deletion")
        return url
