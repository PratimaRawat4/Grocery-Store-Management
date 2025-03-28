from django.urls import path
from . import views
from .views import check_low_stock
from .views import sell_product
from . import views
from .views import generate_invoice,  generate_report


urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_product, name='add_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('invoice/', views.generate_invoice, name='generate_invoice'),
    path("check-low-stock/", check_low_stock, name="check_low_stock"),
    path('sell-product/<int:product_id>/', views.sell_product, name='sell_product'),
    path('invoice/', generate_invoice, name='generate_invoice'),
    path('generate-report/', generate_report, name='generate_report'),


]
