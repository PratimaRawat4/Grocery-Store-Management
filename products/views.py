from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.db.models import F
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Product, Category
import tempfile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product


# Home Page - Display Products & Categories
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def add_product(request):
    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        quantity = request.POST["quantity"]
        expiry_date = request.POST.get("expiry_date", None)  # Get expiry date (nullable)
        
        # Ensure low_stock_threshold is always set
        low_stock_threshold = request.POST.get("low_stock_threshold", 5)  # Default value = 5

        Product.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            expiry_date=expiry_date,
            low_stock_threshold=low_stock_threshold
        )

        return redirect("home")

    return render(request, "index.html")


# Delete a Product
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('home')


# Generate a Simple Sales Report (Placeholder)
def generate_report(request):
    return HttpResponse("Sales Report will be generated here.")


# ✅ Generate Invoice Using ReportLab
def generate_invoice(request):
    # Create a BytesIO buffer to store the PDF
    buffer = BytesIO()

    # Create a PDF object using ReportLab
    p = canvas.Canvas(buffer)
    p.setTitle("Invoice")

    # Add Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Invoice")

    p.setFont("Helvetica", 12)
    p.drawString(100, 770, "Product Name     Price     Quantity")

    # Fetch product data from the database
    products = Product.objects.all()

    # Display product list
    y = 750  # Starting Y position for listing products
    for product in products:
        p.drawString(100, y, f"{product.name}         {product.price}         {product.quantity}")
        y -= 20  # Move down for the next product

    # Finalize the PDF
    p.showPage()
    p.save()

    # Set up response to serve the PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response


# Product List with Low Stock Alert
def product_list(request):
    products = Product.objects.all()
    low_stock_products = Product.objects.filter(quantity__lt=5)  # Fetch low-stock products
    return render(request, "home.html", {"products": products, "low_stock_products": low_stock_products})


# ✅ Check for Low Stock and Send Email Alerts
def check_low_stock(request):
    low_stock_products = Product.objects.filter(quantity__lt=F('low_stock_threshold'))

    if low_stock_products.exists():
        product_list = "\n".join([f"{p.name} - {p.quantity} left" for p in low_stock_products])

        # Send email notification
        send_mail(
            "🚨 Low Stock Alert!",
            f"The following products are low in stock:\n\n{product_list}",
            "tarunchhabra763@gmail.com",  # Replace with your sender email
            ["pcsolutions763@gmail.com"],  # Replace with recipient email
            fail_silently=False,
        )

        return JsonResponse({'status': 'warning', 'message': 'Low stock email sent!'})

    return JsonResponse({'status': 'ok', 'message': 'All products are sufficiently stocked.'})


def sell_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        sell_quantity = int(request.POST.get("quantity", 1))  # Get quantity from form input

        if sell_quantity > product.quantity:
            messages.error(request, "Not enough stock available.")
        else:
            product.quantity -= sell_quantity  # Reduce quantity
            product.save()
            messages.success(request, f"Sold {sell_quantity} {product.name}(s).")

    return redirect("home")  # Redirect to home page instead of another page
