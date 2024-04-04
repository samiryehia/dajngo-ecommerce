# Import necessary Django utilities and model(s)
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    """
    This view returns a list of all products in the database.
    
    The `render` function is used to generate the HTML response. It takes the
    HttpRequest object, a template name, and a context dictionary as arguments.
    The context dictionary contains data that will be made available to the template.
    """

    # Retrieve all Product instances from the database
    products = Product.objects.all()

    # Prepare the context dictionary to pass data to the template
    context = {
        'products': products  # 'products' key will contain the queryset of all products
    }

    # Render and return the response using the 'shop/product_list.html' template
    return render(request, 'shop/product_list.html', context)

def product_detail(request, pk):
    """
    This view returns the details for a specific product identified by its primary key (pk).
    
    The `get_object_or_404` utility is used to get the Product instance with the given pk.
    If no Product with the provided pk is found, an Http404 exception is raised, showing a standard 404 error page.
    """

    # Retrieve the Product instance with the provided pk or raise Http404
    product = get_object_or_404(Product, pk=pk)

    # Prepare the context dictionary
    context = {
        'product': product  # 'product' key will contain the specific Product instance
    }

    # Render and return the response using the 'shop/product_detail.html' template
    return render(request, 'shop/product_detail.html', context)
