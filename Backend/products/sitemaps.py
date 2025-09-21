from django.contrib.sitemaps import Sitemap
from .models import Product

class ProductSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Product.objects.filter(is_available=True).order_by('name')

    def lastmod(self, obj):
        return obj.updated_date