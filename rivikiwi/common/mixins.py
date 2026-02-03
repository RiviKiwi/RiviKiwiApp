from django.http import HttpResponseRedirect
from products.models import City, ProductCategory, ProductImage


class ProductMixin:
    def form_valid(self, form):
        self.images = self.request.FILES.getlist("images")

        if len(self.images) > 10:
            return self.form_invalid(form)

        self.category_sl = self.request.POST.get("category")
        self.city_sl = self.request.POST.get("city")

        new_form = form.save(commit=False)

        try:
            category = ProductCategory.objects.get(slug=self.category_sl)
        except ProductCategory.DoesNotExist:
            form.add_error("category", "Выберите категорию")
            return self.form_invalid(form)
        try:
            city = City.objects.get(slug=self.city_sl)
        except City.DoesNotExist:
            form.add_error("city", "Выберите город")
            return self.form_invalid(form)

        new_form.category = category
        new_form.city = city
        new_form.user = self.request.user
        new_form.save()
        for i, image in enumerate(self.images):
            is_main = True if i == 0 else False
            ProductImage.objects.create(image=image, product=new_form, is_main=is_main)
        return HttpResponseRedirect(self.get_success_url())
